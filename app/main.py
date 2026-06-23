import argparse

from app.scenarios import SCENARIOS
from app.patient_agent import generate_patient_reply
from app.fake_clinic_agent import fake_clinic_response
from app.transcript_utils import save_transcript
from app.audio_utils import create_local_audio_recording
from app.run_context import create_run_id, create_run_directory, save_run_manifest


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


def get_scenario_by_id(scenario_id: str) -> dict:
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario

    available_ids = "\n".join(f"- {scenario['id']}" for scenario in SCENARIOS)
    raise ValueError(
        f"Scenario not found: {scenario_id}\n\n"
        f"Available scenarios:\n{available_ids}"
    )


def run_local_simulation(scenario: dict, max_turns: int = 6) -> None:
    run_id = create_run_id(scenario["id"])
    run_dir = create_run_directory(run_id)

    print(f"\nRunning scenario: {scenario['id']}")
    print(f"Run ID: {run_id}")
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

    save_run_manifest(run_dir, scenario, run_id)
    save_transcript(scenario, turns, run_dir=run_dir)
    create_local_audio_recording(scenario, turns, run_dir=run_dir)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run local patient-agent simulations."
    )

    parser.add_argument(
        "--scenario",
        type=str,
        help="Run only one scenario by scenario ID. If omitted, all scenarios run.",
    )

    args = parser.parse_args()

    if args.scenario:
        scenario = get_scenario_by_id(args.scenario)
        run_local_simulation(scenario)
        return

    for scenario in SCENARIOS:
        run_local_simulation(scenario)


if __name__ == "__main__":
    main()