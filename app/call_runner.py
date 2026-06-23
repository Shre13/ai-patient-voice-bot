import argparse

from app.twilio_client import place_assessment_call


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