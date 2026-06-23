import os
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime, timezone

from dotenv import load_dotenv
from twilio.rest import Client

from app.config import ASSESSMENT_PHONE_NUMBER


@dataclass
class TwilioCallResult:
    dry_run: bool
    to_number: str
    from_number: str | None
    status: str
    scenario_id: str | None = None
    run_id: str | None = None
    run_dir: str | None = None
    call_sid: str | None = None


def validate_assessment_number(to_number: str) -> None:
    """
    Safety guard: the challenge requires calls only to the assessment number.
    This prevents accidental calls to any other number.
    """

    if to_number != ASSESSMENT_PHONE_NUMBER:
        raise ValueError(
            f"Blocked outbound call to {to_number}. "
            f"Only {ASSESSMENT_PHONE_NUMBER} is allowed."
        )


def get_twilio_client() -> Client:
    load_dotenv()

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        raise RuntimeError(
            "Missing Twilio credentials. Add TWILIO_ACCOUNT_SID and "
            "TWILIO_AUTH_TOKEN to your local .env file."
        )

    return Client(account_sid, auth_token)


def save_twilio_call_plan(
    run_dir: Path,
    scenario_id: str,
    run_id: str,
    to_number: str,
    from_number: str,
    dry_run: bool,
    call_sid: str | None = None,
) -> None:
    """
    Saves the planned or completed Twilio call setup for traceability.
    """

    call_plan_path = run_dir / "twilio_call_plan.json"

    call_plan = {
        "scenario_id": scenario_id,
        "run_id": run_id,
        "to_number": to_number,
        "from_number": from_number,
        "dry_run": dry_run,
        "call_sid": call_sid,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    with call_plan_path.open("w", encoding="utf-8") as file:
        json.dump(call_plan, file, indent=2)

    print(f"Saved Twilio call plan: {call_plan_path}")


def place_assessment_call(
    scenario_id: str,
    run_id: str,
    run_dir: Path,
    dry_run: bool = True,
) -> TwilioCallResult:
    """
    Prepare or place the outbound assessment call.

    dry_run=True does not call Twilio. It only validates config and prints
    what would happen. Use dry_run=False only when ready to make real calls.
    """

    load_dotenv()

    to_number = ASSESSMENT_PHONE_NUMBER
    from_number = os.getenv("TWILIO_PHONE_NUMBER")

    validate_assessment_number(to_number)

    if not from_number:
        raise RuntimeError(
            "Missing TWILIO_PHONE_NUMBER. Add your Twilio number to .env "
            "before making or dry-running calls."
        )

    if dry_run:
        save_twilio_call_plan(
            run_dir=run_dir,
            scenario_id=scenario_id,
            run_id=run_id,
            to_number=to_number,
            from_number=from_number,
            dry_run=True,
        )

        return TwilioCallResult(
            dry_run=True,
            to_number=to_number,
            from_number=from_number,
            status="dry_run_validated",
            scenario_id=scenario_id,
            run_id=run_id,
            run_dir=str(run_dir),
            call_sid=None,
        )

    public_webhook_base_url = os.getenv("PUBLIC_WEBHOOK_BASE_URL")

    if not public_webhook_base_url:
        raise RuntimeError(
            "Missing PUBLIC_WEBHOOK_BASE_URL. Start your local webhook server, "
            "expose it with a tunnel, and add the public URL to .env before making a real call."
        )

    client = get_twilio_client()

    base_url = public_webhook_base_url.rstrip("/")
    voice_webhook_url = f"{base_url}/voice"
    status_callback_url = f"{base_url}/status-callback"
    recording_callback_url = f"{base_url}/recording-callback"

    call = client.calls.create(
        to=to_number,
        from_=from_number,
        url=voice_webhook_url,
        record=True,
        recording_status_callback=recording_callback_url,
        status_callback=status_callback_url,
        status_callback_event=["initiated", "ringing", "answered", "completed"],
    )

    save_twilio_call_plan(
        run_dir=run_dir,
        scenario_id=scenario_id,
        run_id=run_id,
        to_number=to_number,
        from_number=from_number,
        dry_run=False,
        call_sid=call.sid,
    )

    return TwilioCallResult(
        dry_run=False,
        to_number=to_number,
        from_number=from_number,
        status=call.status,
        scenario_id=scenario_id,
        run_id=run_id,
        run_dir=str(run_dir),
        call_sid=call.sid,
    )