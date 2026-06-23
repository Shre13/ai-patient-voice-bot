from pathlib import Path
from datetime import datetime, timezone
import json

from flask import Flask, Response, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)


def save_webhook_event(event_type: str, payload: dict) -> None:
    """
    Saves Twilio webhook events locally for debugging.

    This is useful during real-call testing because Twilio sends call status,
    recording, and call metadata through webhook requests.
    """

    events_dir = Path("calls") / "_twilio_events"
    events_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    event_path = events_dir / f"{timestamp}_{event_type}.json"

    event_data = {
        "event_type": event_type,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }

    with event_path.open("w", encoding="utf-8") as file:
        json.dump(event_data, file, indent=2)

    print(f"Saved webhook event: {event_path}")


@app.route("/health", methods=["GET"])
def health_check() -> dict:
    return {"status": "ok"}


@app.route("/voice", methods=["POST", "GET"])
def voice_webhook() -> Response:
    """
    Basic Twilio voice webhook.

    This is a placeholder for the real voice-bot integration. For now, it proves
    that the app can return valid TwiML instructions to Twilio.
    """

    save_webhook_event("voice_webhook", dict(request.values))

    response = VoiceResponse()

    response.say(
        "Hello. This is the local patient bot webhook. "
        "The real voice agent integration will be connected in the next phase.",
        voice="alice",
    )

    response.pause(length=1)

    response.say(
        "This call is ending now because this is only a webhook test.",
        voice="alice",
    )

    response.hangup()

    return Response(str(response), mimetype="text/xml")


@app.route("/status-callback", methods=["POST"])
def status_callback() -> dict:
    """
    Receives Twilio call lifecycle updates.

    Example statuses include queued, ringing, in-progress, completed, busy,
    failed, or no-answer.
    """

    save_webhook_event("status_callback", dict(request.values))
    return {"status": "received"}


@app.route("/recording-callback", methods=["POST"])
def recording_callback() -> dict:
    """
    Receives Twilio recording metadata after a call recording is available.

    Later, this endpoint can be extended to download the recording and attach it
    to the correct scenario folder.
    """

    save_webhook_event("recording_callback", dict(request.values))
    return {"status": "received"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)