import argparse

from app.config import ASSESSMENT_PHONE_NUMBER
from app.scenarios import SCENARIOS
from app.run_context import create_run_id, create_run_directory
from app.twilio_client import place_assessment_call
from app.preflight import run_preflight

CONFIRMATION_TEXT = "CALL_ASSESSMENT_LINE"


def get_scenario_by_id(scenario_id: str) -> dict:
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario

    available_ids = "\n".join(f"- {scenario['id']}" for scenario in SCENARIOS)
    raise ValueError(
        f"Scenario not found: {scenario_id}\n\n"
        f"Available scenarios:\n{available_ids}"
    )


def confirm_real_call() -> None:
    """
    Extra safety step before making a real outbound call.

    This prevents accidental paid calls while developing locally.
    """

    print("\nYou are about to place a REAL outbound call.")
    print(f"Destination: {ASSESSMENT_PHONE_NUMBER}")
    print("This may create Twilio/API charges.")
    print(f'Type "{CONFIRMATION_TEXT}" to continue.')

    user_input = input("Confirmation: ").strip()

    if user_input != CONFIRMATION_TEXT:
        raise RuntimeError("Real call cancelled. Confirmation text did not match.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Twilio assessment call setup."
    )

    parser.add_argument(
        "--scenario",
        required=True,
        type=str,
        help="Scenario ID to associate with this Twilio call.",
    )

    parser.add_argument(
        "--real-call",
        action="store_true",
        help="Actually place the assessment call. Default is dry-run only.",
    )

    args = parser.parse_args()

    run_preflight(
    scenario_id=args.scenario,
    real_call=args.real_call,
)

    scenario = get_scenario_by_id(args.scenario)
    run_id = create_run_id(scenario["id"])
    run_dir = create_run_directory(run_id)

    print(f"Scenario: {scenario['id']}")
    print(f"Run ID: {run_id}")
    print(f"Run directory: {run_dir}")

    if args.real_call:
        confirm_real_call()

    result = place_assessment_call(
        scenario_id=scenario["id"],
        run_id=run_id,
        run_dir=run_dir,
        dry_run=not args.real_call,
    )

    print("\nTwilio call setup result")
    print(f"Dry run: {result.dry_run}")
    print(f"Scenario ID: {result.scenario_id}")
    print(f"Run ID: {result.run_id}")
    print(f"Run directory: {result.run_dir}")
    print(f"To: {result.to_number}")
    print(f"From: {result.from_number}")
    print(f"Status: {result.status}")

    if result.call_sid:
        print(f"Call SID: {result.call_sid}")


if __name__ == "__main__":
    main()