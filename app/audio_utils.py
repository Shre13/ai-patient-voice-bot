from pathlib import Path
import pyttsx3


def create_local_audio_recording(
    scenario: dict,
    turns: list[dict],
    run_dir: Path | None = None
) -> None:
    """
    Creates a local simulated call recording from transcript turns.

    This is only for local development. Real assessment recordings will come
    from the actual phone-call integration later.
    """

    call_dir = run_dir or (Path("calls") / scenario["id"])
    call_dir.mkdir(parents=True, exist_ok=True)

    recording_path = call_dir / "local_simulated_recording.wav"

    engine = pyttsx3.init()
    engine.setProperty("rate", 165)

    spoken_lines = []

    for turn in turns:
        speaker = turn["speaker"]
        text = turn["text"]
        spoken_lines.append(f"{speaker} says: {text}")

    full_text = " ".join(spoken_lines)

    engine.save_to_file(full_text, str(recording_path))
    engine.runAndWait()

    print(f"Saved local audio: {recording_path}")