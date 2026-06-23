# Iteration Notes

## Phase 1: Local simulation

I started with a local-only simulation instead of immediately connecting to paid telephony APIs. This made it easier to test the scenario design, patient behavior, transcript saving, and folder structure before making real calls.

## First issue found

The first local version produced repetitive conversations. Several scenarios got stuck in loops where the clinic agent repeatedly asked for more detail and the patient bot repeated a generic response.

## Change made

I updated the fake clinic agent and patient agent to add scenario-specific exits. For example, the urgent symptom scenario now ends after the patient agrees to seek urgent care, and the insurance/location/weekend scenarios now close naturally after the agent gives the relevant guidance.

## Result

The second local run produced cleaner transcripts for all 10 scenarios. The conversations are still intentionally simple because this phase is only meant to validate flow before real voice-call integration.

## Phase 2: Local audio artifacts

After the text simulation worked, I added local simulated audio generation using `pyttsx3`. This is not meant to replace the real phone recordings required by the challenge. It is a development step that lets me test the call artifact structure locally before paying for telephony/API calls.

The local audio files are intentionally labeled `local_simulated_recording.wav` so they are not confused with final assessment recordings.

## Phase 3: Twilio webhook skeleton

I added a local Flask webhook that returns valid TwiML. This is a preparation step before making real calls. The current webhook only says a placeholder message and hangs up, which lets me test the Twilio-facing structure without spending money or calling the assessment line.

## Phase 4: Real-call safety guard

I added an explicit confirmation step before allowing a real outbound call. Dry-run mode remains the default. If `--real-call` is used, the script requires the exact confirmation text before calling Twilio. This reduces the chance of accidental paid calls during development.