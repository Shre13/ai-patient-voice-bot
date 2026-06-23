from pathlib import Path
from datetime import datetime, timezone
import json


def save_transcript(scenario: dict, turns: list[dict]) -> None:
    call_dir = Path("calls") / scenario["id"]
    call_dir.mkdir(parents=True, exist_ok=True)

    transcript_path = call_dir / "transcript.txt"
    metadata_path = call_dir / "metadata.json"

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
        "local_simulation": True
    }

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    print(f"Saved transcript: {transcript_path}")