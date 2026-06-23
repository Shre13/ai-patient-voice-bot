import argparse

from app.config import ASSESSMENT_PHONE_NUMBER
from app.twilio_client import place_assessment_call


CONFIRMATION_TEXT = "CALL_ASSESSMENT_LINE"


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
        "--real-call",
        action="store_true",
        help="Actually place the assessment call. Default is dry-run only.",
    )

    args = parser.parse_args()

    if args.real_call:
        confirm_real_call()

    result = place_assessment_call(dry_run=not args.real_call)

    print("Twilio call setup result")
    print(f"Dry run: {result.dry_run}")
    print(f"To: {result.to_number}")
    print(f"From: {result.from_number}")
    print(f"Status: {result.status}")

    if result.call_sid:
        print(f"Call SID: {result.call_sid}")


if __name__ == "__main__":
    main()