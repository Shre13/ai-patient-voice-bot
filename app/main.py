from app.scenarios import SCENARIOS
from app.patient_agent import generate_patient_reply
from app.fake_clinic_agent import fake_clinic_response
from app.transcript_utils import save_transcript
from app.audio_utils import create_local_audio_recording

CLOSING_PHRASES = [
    "thank you for your help",
    "that answers my question",
    "i will seek urgent care",
    "i will call 911",
    "i understand"
]


def should_end_conversation(patient_reply: str) -> bool:
    reply = patient_reply.lower()
    return any(phrase in reply for phrase in CLOSING_PHRASES)


def run_local_simulation(scenario: dict, max_turns: int = 6) -> None:
    print(f"\nRunning scenario: {scenario['id']}")
    print(f"Goal: {scenario['goal']}\n")

    turns = []

    clinic_message = fake_clinic_response("", 0)
    turns.append({"speaker": "Clinic Agent", "text": clinic_message})
    print(f"Clinic Agent: {clinic_message}")

    for turn_number in range(max_turns):
        patient_reply = generate_patient_reply(
            scenario=scenario,
            clinic_message=clinic_message,
            turn_number=turn_number
        )

        turns.append({"speaker": "Patient Bot", "text": patient_reply})
        print(f"Patient Bot: {patient_reply}")

        if should_end_conversation(patient_reply):
            break

        clinic_message = fake_clinic_response(patient_reply, turn_number + 1)
        turns.append({"speaker": "Clinic Agent", "text": clinic_message})
        print(f"Clinic Agent: {clinic_message}")

    save_transcript(scenario, turns)
    create_local_audio_recording(scenario, turns)


def main() -> None:
    for scenario in SCENARIOS:
        run_local_simulation(scenario)


if __name__ == "__main__":
    main()