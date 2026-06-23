import os
from dataclasses import dataclass

from dotenv import load_dotenv
from twilio.rest import Client

from app.config import ASSESSMENT_PHONE_NUMBER


@dataclass
class TwilioCallResult:
    dry_run: bool
    to_number: str
    from_number: str | None
    status: str
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


def place_assessment_call(dry_run: bool = True) -> TwilioCallResult:
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
        return TwilioCallResult(
            dry_run=True,
            to_number=to_number,
            from_number=from_number,
            status="dry_run_validated",
            call_sid=None,
        )

    client = get_twilio_client()

    # Placeholder TwiML URL.
    # Later, this will point to our local/public webhook that controls the voice bot.
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        url="https://demo.twilio.com/docs/voice.xml",
        record=True,
    )

    return TwilioCallResult(
        dry_run=False,
        to_number=to_number,
        from_number=from_number,
        status=call.status,
        call_sid=call.sid,
    )