from datetime import datetime, timezone
from pathlib import Path
import json


def create_run_id(scenario_id: str) -> str:
    """
    Creates a unique run ID for a scenario execution.

    Example:
    20260622T231530Z_call_05_weekend_request
    """

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}_{scenario_id}"


def create_run_directory(run_id: str) -> Path:
    """
    Creates a directory for a single scenario run.
    """

    run_dir = Path("calls") / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def save_run_manifest(run_dir: Path, scenario: dict, run_id: str) -> None:
    """
    Saves run-level metadata so each call can be traced back to a scenario.
    """

    manifest_path = run_dir / "run_manifest.json"

    manifest = {
        "run_id": run_id,
        "scenario_id": scenario["id"],
        "persona": scenario["persona"],
        "goal": scenario["goal"],
        "expected_behavior": scenario["expected_behavior"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "local_simulation",
        "twilio_call_sid": None,
        "recording_file": None,
        "transcript_file": "transcript.txt",
        "notes_file": "notes.md"
    }

    with manifest_path.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=2)

    print(f"Saved run manifest: {manifest_path}")