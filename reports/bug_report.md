# Bug Report

## Overview

This report summarizes bugs and implementation issues discovered while testing the AI patient voice bot against the assessment phone line. The project followed a staged workflow: local simulation, Twilio dry-run validation, real outbound calls, transcript capture, recording capture, and final artifact preparation.

## Bug 1: Recording disclosure caused generic patient response

### Scenario

The clinic AI opened the call with a recording disclosure.

### Observed Behavior

The patient bot responded generically instead of continuing the scenario goal.

### Expected Behavior

The patient bot should acknowledge the disclosure and continue with the original reason for calling.

### Fix

Added detection for recording disclosure phrases such as “call may be recorded,” “recorded for quality,” and “quality and training.” When detected, the bot repeats the scenario’s patient opening.

---

## Bug 2: Demo patient profile prompt caused weak fallback response

### Scenario

The clinic AI asked if the caller wanted to create a demo patient profile.

### Observed Behavior

The bot gave a generic next-step response.

### Expected Behavior

The bot should agree and provide basic demo patient details.

### Fix

Added handling for demo profile prompts. The bot now provides a demo name and date of birth.

---

## Bug 3: Webhook event logs could overwrite each other

### Scenario

Twilio sent multiple callbacks close together.

### Observed Behavior

Webhook event filenames used second-level timestamps, which could overwrite events of the same type.

### Expected Behavior

Each webhook event should be saved uniquely.

### Fix

Updated webhook event filenames to include microseconds.

---

## Bug 4: Recording metadata was not initially saved into each run folder

### Scenario

The recording callback was received after a real call.

### Observed Behavior

The callback event was saved globally, but the run folder did not initially get clean recording metadata.

### Expected Behavior

Each call run folder should include recording SID, recording URL, duration, and status.

### Fix

Updated the recording callback route to write `recording_metadata.json` into the run-specific call folder.

---

## Bug 5: One medication refill call produced incomplete artifacts on first attempt

### Scenario

The first `call_04_medication_refill` real call only created the Twilio call plan.

### Observed Behavior

The folder was missing transcript and recording metadata.

### Expected Behavior

Each final call should include transcript and recording metadata.

### Fix

Checked Twilio event logs, discarded the incomplete run, and reran only that scenario. The completed rerun was used in `final_calls`.

---

## Final Artifact Status

The final submission includes 10 selected call folders under `final_calls/`.

Each folder contains:

- `recording.mp3`
- `transcript.txt`
- `metadata.json`
- `notes.md`