from pathlib import Path
from datetime import datetime, timezone
import json

from flask import Flask, Response, request
from twilio.twiml.voice_response import VoiceResponse, Gather

from app.scenarios import SCENARIOS
from app.patient_agent import generate_patient_reply


app = Flask(__name__)


def get_scenario_by_id(scenario_id: str) -> dict:
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario

    return SCENARIOS[0]


def save_webhook_event(event_type: str, payload: dict) -> None:
    events_dir = Path("calls") / "_twilio_events"
    events_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    event_path = events_dir / f"{timestamp}_{event_type}.json"

    event_data = {
        "event_type": event_type,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }

    with event_path.open("w", encoding="utf-8") as file:
        json.dump(event_data, file, indent=2)

    print(f"Saved webhook event: {event_path}")


def append_turn_log(run_id: str, speaker: str, text: str) -> None:
    if not run_id:
        run_id = "unknown_run"

    call_dir = Path("calls") / run_id
    call_dir.mkdir(parents=True, exist_ok=True)

    transcript_path = call_dir / "live_transcript.txt"

    with transcript_path.open("a", encoding="utf-8") as file:
        file.write(f"{speaker}: {text}\n\n")


@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok"}


@app.route("/voice", methods=["POST", "GET"])
def voice():
    payload = dict(request.values)
    save_webhook_event("voice_webhook", payload)

    scenario_id = request.values.get("scenario_id", "call_01_simple_scheduling")
    run_id = request.values.get("run_id", "manual_browser_test")
    scenario = get_scenario_by_id(scenario_id)

    opening_line = scenario["patient_opening"]
    append_turn_log(run_id, "Patient Bot", opening_line)

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action=f"/respond?scenario_id={scenario_id}&run_id={run_id}&turn=1",
        method="POST",
        speech_timeout="auto",
        timeout=6,
    )

    gather.say(opening_line, voice="alice")
    response.append(gather)

    response.say("I did not hear anything. I will end the call now.", voice="alice")
    response.hangup()

    return Response(str(response), mimetype="text/xml")


@app.route("/respond", methods=["POST"])
def respond():
    payload = dict(request.values)
    save_webhook_event("respond_webhook", payload)

    scenario_id = request.values.get("scenario_id", "call_01_simple_scheduling")
    run_id = request.values.get("run_id", "manual_browser_test")
    turn = int(request.values.get("turn", "1"))

    scenario = get_scenario_by_id(scenario_id)
    clinic_speech = request.values.get("SpeechResult", "")

    if not clinic_speech:
        patient_reply = "Sorry, I could not hear that clearly. Could you repeat that?"
    else:
        append_turn_log(run_id, "Clinic AI", clinic_speech)

        patient_reply = generate_patient_reply(
            scenario=scenario,
            clinic_message=clinic_speech,
            turn_number=turn,
        )

    append_turn_log(run_id, "Patient Bot", patient_reply)

    response = VoiceResponse()

    if turn >= 6 or "thank you" in patient_reply.lower() or "urgent care" in patient_reply.lower():
        response.say(patient_reply, voice="alice")
        response.say("Thank you. Goodbye.", voice="alice")
        response.hangup()
        return Response(str(response), mimetype="text/xml")

    next_turn = turn + 1

    gather = Gather(
        input="speech",
        action=f"/respond?scenario_id={scenario_id}&run_id={run_id}&turn={next_turn}",
        method="POST",
        speech_timeout="auto",
        timeout=6,
    )

    gather.say(patient_reply, voice="alice")
    response.append(gather)

    response.say("I did not hear anything else. I will end the call now.", voice="alice")
    response.hangup()

    return Response(str(response), mimetype="text/xml")


@app.route("/status-callback", methods=["POST"])
def status_callback():
    save_webhook_event("status_callback", dict(request.values))
    return {"status": "received"}


@app.route("/recording-callback", methods=["POST"])
def recording_callback():
    payload = dict(request.values)
    save_webhook_event("recording_callback", payload)

    run_id = payload.get("run_id")

    if run_id:
        call_dir = Path("calls") / run_id
        call_dir.mkdir(parents=True, exist_ok=True)

        recording_metadata_path = call_dir / "recording_metadata.json"

        recording_metadata = {
            "call_sid": payload.get("CallSid"),
            "recording_sid": payload.get("RecordingSid"),
            "recording_url": payload.get("RecordingUrl"),
            "recording_status": payload.get("RecordingStatus"),
            "recording_duration": payload.get("RecordingDuration"),
            "recording_channels": payload.get("RecordingChannels"),
            "recording_source": payload.get("RecordingSource"),
            "received_at": datetime.now(timezone.utc).isoformat(),
        }

        with recording_metadata_path.open("w", encoding="utf-8") as file:
            json.dump(recording_metadata, file, indent=2)

        print(f"Saved recording metadata: {recording_metadata_path}")

    return {"status": "received"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)