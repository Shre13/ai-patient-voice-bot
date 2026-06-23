# Iteration Notes

## Phase 1: Local simulation

I started with a local-only simulation instead of immediately connecting to paid telephony APIs. This made it easier to test the scenario design, patient behavior, transcript saving, and folder structure before making real calls.

Run all local scenarios:

```bash
python -m app.main
```

Run one scenario:

```bash
python -m app.main --scenario call_05_weekend_request
```

## First issue found

The first local version produced repetitive conversations. Several scenarios got stuck in loops where the clinic agent repeatedly asked for more detail and the patient bot repeated a generic response.

## Change made

I updated the fake clinic agent and patient agent to add scenario-specific exits. For example, the urgent symptom scenario now ends after the patient agrees to seek urgent care, and the insurance, location, and weekend scenarios now close naturally after the agent gives the relevant guidance.

## Result

The second local run produced cleaner transcripts for all 10 scenarios. The conversations are still intentionally simple because this phase is only meant to validate flow before real voice-call integration.

## Phase 2: Local audio artifacts

After the text simulation worked, I added local simulated audio generation using `pyttsx3`. This is not meant to replace the real phone recordings required by the challenge. It is a development step that lets me test the call artifact structure locally before paying for telephony or API calls.

The local audio files are intentionally labeled `local_simulated_recording.wav` so they are not confused with final assessment recordings.

## Phase 3: Twilio webhook skeleton

I added a local Flask webhook that returns valid TwiML. This is a preparation step before making real calls. The current webhook only says a placeholder message and hangs up, which lets me test the Twilio-facing structure without spending money or calling the assessment line.

## Phase 4: Real-call safety guard

I added an explicit confirmation step before allowing a real outbound call. Dry-run mode remains the default. If `--real-call` is used, the script requires the exact confirmation text before calling Twilio. This reduces the chance of accidental paid calls during development.

## Phase 5: Twilio callback endpoints

I added placeholder endpoints for Twilio call status and recording callbacks. These endpoints save incoming webhook payloads locally so I can debug call lifecycle events before building the full recording and transcription pipeline. This also helps connect real call artifacts back to each assessment run later.

## Phase 6: Scenario run IDs

I added run-specific folders so each scenario execution gets a unique ID. This makes it easier to connect a future Twilio call SID, recording, transcript, and notes back to the exact scenario being tested. This is especially important once multiple real calls are made for the same scenario or when early calls need to be separated from final selected calls.

## Phase 7: Single-scenario runner

I added a command-line option to run one scenario at a time. This makes local testing faster and prepares the project for real call testing, where each Twilio call should be tied to one specific scenario and run ID.

## Phase 8: Scenario-aware Twilio dry-run

I updated the Twilio call runner so every planned call must be associated with a scenario ID. Dry-run mode now creates a `twilio_call_plan.json` file inside a run-specific folder, which makes it easier to connect each future real call to a scenario, recording, transcript, and bug report entry.

Example dry-run command:

```bash
python -m app.call_runner --scenario call_05_weekend_request

## Phase 9: Final call artifact separation

I separated local development call artifacts from final assessment call artifacts. Local runs stay under `calls/` and are ignored to avoid cluttering the repo, while selected final calls will be copied into `final_calls/` for submission. This keeps the repository cleaner and makes the required deliverables easier to review.

## Phase 10: Public tunnel preparation

I documented the tunnel setup needed for Twilio to reach the local Flask webhook. This is still a preparation step and does not place a real call. The goal is to make the real-call setup repeatable by clearly documenting how to expose `/voice`, `/status-callback`, and `/recording-callback` through a public HTTPS URL.

## Phase 11: Preflight checks

I added a preflight command to validate the scenario ID, `.env` file, Twilio phone number, assessment-number safety guard, and public webhook URL requirements before making calls. Dry-run mode allows an empty public webhook URL, while real-call mode requires it. This gives me a safer checklist before spending money on telephony calls.