from pathlib import Path
from datetime import datetime, timezone
import json


def save_transcript(scenario: dict, turns: list[dict], run_dir: Path | None = None) -> None:
    """
    Saves transcript, metadata, and review notes for a scenario run.

    If run_dir is provided, artifacts are saved inside that run-specific folder.
    Otherwise, it falls back to calls/<scenario_id>.
    """

    call_dir = run_dir or (Path("calls") / scenario["id"])
    call_dir.mkdir(parents=True, exist_ok=True)

    transcript_path = call_dir / "transcript.txt"
    metadata_path = call_dir / "metadata.json"
    notes_path = call_dir / "notes.md"

    with transcript_path.open("w", encoding="utf-8") as file:
        file.write(f"Scenario: {scenario['id']}\n")
        file.write(f"Persona: {scenario['persona']}\n")
        file.write(f"Goal: {scenario['goal']}\n")
        file.write(f"Expected Behavior: {scenario['expected_behavior']}\n")
        file.write("\n--- Transcript ---\n\n")

        for turn in turns:
            file.write(f"{turn['speaker']}: {turn['text']}\n\n")

    metadata = {
        "scenario_id": scenario["id"],
        "persona": scenario["persona"],
        "goal": scenario["goal"],
        "expected_behavior": scenario["expected_behavior"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "turn_count": len(turns),
        "local_simulation": True,
        "recording_file": "local_simulated_recording.wav",
        "transcript_file": "transcript.txt",
        "notes_file": "notes.md"
    }

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    if not notes_path.exists():
        with notes_path.open("w", encoding="utf-8") as file:
            file.write(f"# Notes: {scenario['id']}\n\n")
            file.write(f"## Scenario Goal\n\n{scenario['goal']}\n\n")
            file.write("## What to Listen For\n\n")
            file.write(f"- {scenario['expected_behavior']}\n")
            file.write("- Did the conversation sound natural?\n")
            file.write("- Did the agent ask appropriate clarifying questions?\n")
            file.write("- Did the agent avoid unsafe or unsupported claims?\n\n")
            file.write("## Observations\n\n")
            file.write("- TBD after real call review.\n\n")
            file.write("## Potential Bug\n\n")
            file.write("- TBD.\n")

    print(f"Saved transcript: {transcript_path}")