import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from app.config import ASSESSMENT_PHONE_NUMBER
from app.scenarios import SCENARIOS


EXPECTED_ASSESSMENT_NUMBER = "+18054398008"


def get_scenario_by_id(scenario_id: str) -> dict:
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario

    available_ids = "\n".join(f"- {scenario['id']}" for scenario in SCENARIOS)
    raise ValueError(
        f"Scenario not found: {scenario_id}\n\n"
        f"Available scenarios:\n{available_ids}"
    )


def check_env_file() -> None:
    env_path = Path(".env")

    if not env_path.exists():
        raise RuntimeError("Missing .env file. Create one from .env.example.")

    print("PASS: .env file exists")


def check_assessment_number() -> None:
    if ASSESSMENT_PHONE_NUMBER != EXPECTED_ASSESSMENT_NUMBER:
        raise RuntimeError(
            f"Assessment number mismatch. Expected {EXPECTED_ASSESSMENT_NUMBER}, "
            f"found {ASSESSMENT_PHONE_NUMBER}."
        )

    print(f"PASS: assessment number safety guard is set to {ASSESSMENT_PHONE_NUMBER}")


def check_twilio_phone_number() -> None:
    twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not twilio_phone_number:
        raise RuntimeError("Missing TWILIO_PHONE_NUMBER in .env")

    if not twilio_phone_number.startswith("+"):
        raise RuntimeError("TWILIO_PHONE_NUMBER should be in E.164 format, e.g. +15555550123")

    print(f"PASS: TWILIO_PHONE_NUMBER is present: {twilio_phone_number}")


def check_public_webhook_url(required: bool) -> None:
    public_webhook_base_url = os.getenv("PUBLIC_WEBHOOK_BASE_URL")

    if not public_webhook_base_url:
        if required:
            raise RuntimeError(
                "Missing PUBLIC_WEBHOOK_BASE_URL in .env. "
                "This is required before making a real call."
            )

        print("WARN: PUBLIC_WEBHOOK_BASE_URL is empty. This is okay for dry-run.")
        return

    if public_webhook_base_url.endswith("/voice"):
        raise RuntimeError(
            "PUBLIC_WEBHOOK_BASE_URL should not include /voice. "
            "Use only the base URL."
        )

    if not public_webhook_base_url.startswith("https://"):
        raise RuntimeError("PUBLIC_WEBHOOK_BASE_URL should be a public HTTPS URL.")

    print(f"PASS: PUBLIC_WEBHOOK_BASE_URL is set: {public_webhook_base_url}")


def run_preflight(scenario_id: str, real_call: bool) -> None:
    print("Running preflight checks...\n")

    load_dotenv()

    scenario = get_scenario_by_id(scenario_id)
    print(f"PASS: scenario exists: {scenario['id']}")

    check_env_file()
    check_assessment_number()
    check_twilio_phone_number()
    check_public_webhook_url(required=real_call)

    print("\nPreflight complete.")

    if real_call:
        print("Result: setup looks ready for a real call.")
    else:
        print("Result: setup looks ready for dry-run.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run setup checks before Twilio dry-run or real calls."
    )

    parser.add_argument(
        "--scenario",
        required=True,
        type=str,
        help="Scenario ID to validate.",
    )

    parser.add_argument(
        "--real-call",
        action="store_true",
        help="Require checks needed for a real call.",
    )

    args = parser.parse_args()

    run_preflight(
        scenario_id=args.scenario,
        real_call=args.real_call,
    )


if __name__ == "__main__":
    main()