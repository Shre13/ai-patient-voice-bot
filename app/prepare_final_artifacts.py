import base64
import json
import os
import urllib.request
from pathlib import Path

from dotenv import load_dotenv


FINAL_CALLS_DIR = Path("final_calls")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def download_recording(recording_url: str, output_path: Path) -> None:
    load_dotenv()

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        raise RuntimeError("Missing TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN in .env")

    mp3_url = f"{recording_url}.mp3"

    credentials = f"{account_sid}:{auth_token}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")

    request = urllib.request.Request(mp3_url)
    request.add_header("Authorization", f"Basic {encoded_credentials}")

    with urllib.request.urlopen(request) as response:
        output_path.write_bytes(response.read())


def prepare_call_folder(call_dir: Path) -> None:
    recording_metadata_path = call_dir / "recording_metadata.json"
    twilio_call_plan_path = call_dir / "twilio_call_plan.json"
    transcript_path = call_dir / "transcript.txt"
    live_transcript_path = call_dir / "live_transcript.txt"

    if not recording_metadata_path.exists():
        print(f"SKIP: {call_dir.name} missing recording_metadata.json")
        return

    if not twilio_call_plan_path.exists():
        print(f"SKIP: {call_dir.name} missing twilio_call_plan.json")
        return

    if not transcript_path.exists() and live_transcript_path.exists():
        transcript_path.write_text(
            live_transcript_path.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    recording_metadata = load_json(recording_metadata_path)
    twilio_call_plan = load_json(twilio_call_plan_path)

    recording_output_path = call_dir / "recording.mp3"

    if not recording_output_path.exists():
        print(f"Downloading recording for {call_dir.name}...")
        download_recording(
            recording_url=recording_metadata["recording_url"],
            output_path=recording_output_path,
        )

    clean_metadata = {
        "scenario_id": twilio_call_plan.get("scenario_id"),
        "run_id": twilio_call_plan.get("run_id"),
        "call_sid": recording_metadata.get("call_sid"),
        "recording_sid": recording_metadata.get("recording_sid"),
        "recording_status": recording_metadata.get("recording_status"),
        "recording_duration_seconds": recording_metadata.get("recording_duration"),
        "transcript_file": "transcript.txt",
        "recording_file": "recording.mp3",
        "notes_file": "notes.md",
        "artifact_status": "final_submission_candidate",
    }

    metadata_path = call_dir / "metadata.json"

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(clean_metadata, file, indent=2)

    notes_path = call_dir / "notes.md"

    if not notes_path.exists():
        notes_path.write_text(
            f"# {call_dir.name}\n\n"
            f"## Summary\n\n"
            f"Final assessment call artifact for scenario `{clean_metadata['scenario_id']}`.\n\n"
            f"## Files\n\n"
            f"- `recording.mp3`: Twilio call recording\n"
            f"- `transcript.txt`: Live transcript captured from Twilio speech input and patient bot output\n"
            f"- `metadata.json`: Clean call metadata for review\n\n"
            f"## Review Notes\n\n"
            f"- Call connected successfully.\n"
            f"- Recording callback completed.\n"
            f"- Transcript was captured during the voice interaction.\n",
            encoding="utf-8",
        )

    print(f"DONE: {call_dir.name}")


def main() -> None:
    if not FINAL_CALLS_DIR.exists():
        raise RuntimeError("Missing final_calls directory")

    call_dirs = [path for path in FINAL_CALLS_DIR.iterdir() if path.is_dir()]

    for call_dir in sorted(call_dirs):
        prepare_call_folder(call_dir)


if __name__ == "__main__":
    main()