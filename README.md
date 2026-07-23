# AI Voice Agent Testing Framework

An automated testing framework that places real outbound phone calls to a healthcare voice AI agent, simulates realistic patient scenarios, and surfaces bugs and quality issues through transcript analysis. Built in Python using Twilio for call automation and webhook handling.

## Background

This project was built for a technical assessment for an AI voice-agent company, which asked candidates to design an automated "patient" caller to stress-test their production clinic scheduling agent. Rather than treating it as a scripted benchmark runner, I focused on making the caller behave like a real user, natural turn-taking, realistic pacing, and active steering toward specific test outcomes, so the bugs it surfaced would reflect genuine conversational failure modes, not just scripted edge cases.

## What It Does

- Places outbound calls via Twilio to a target voice AI agent
- Runs 10 distinct patient scenarios: simple scheduling, rescheduling, cancellation, medication refills, weekend availability requests, insurance questions, location questions, unclear/ambiguous requests, mid-call interruptions, and urgent symptom triage
- Captures full call recordings and transcripts for every scenario
- Includes dry-run and preflight validation modes to catch configuration issues before placing real (billable) calls
- Downloads and organizes final call artifacts (recording, transcript, metadata, notes) per scenario for review

## Key Findings

Through real-call testing, I identified and documented several issues in the agent's conversational logic, including:
- Inconsistent handling of demo patient profile creation and date-of-birth verification
- Incorrect availability logic (agent did not always correctly flag when requested times fell outside business hours)
- Gaps in recording-disclosure consistency across calls
- An incomplete medication-refill flow that required a rerun to capture cleanly

Full write-up: [`reports/bug_report.md`](reports/bug_report.md)

## Architecture

The system has three main layers:
1. **Call orchestration** (`app/call_runner.py`, `app/preflight.py`) — validates configuration, manages dry-run vs. real-call modes, and requires explicit confirmation before placing real calls to avoid accidental dialing.
2. **Webhook handling** (`app/webhook_server.py`) — a Flask server that receives Twilio call events and drives the conversation in real time.
3. **Artifact pipeline** (`app/prepare_final_artifacts.py`) — downloads recordings and organizes transcripts/metadata into a consistent per-scenario structure for review and analysis.

Design choices prioritized safety (hard-coded target number to prevent misdials, explicit confirmation phrase before real calls) and reproducibility (structured artifacts, dry-run mode for iteration without cost).

## Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` with your Twilio credentials:
```
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
PUBLIC_WEBHOOK_BASE_URL=
```

## Usage

Run a local simulation:
```bash
python -m app.main --scenario call_05_weekend_request
```

Start the webhook server (for real calls, expose via a public HTTPS tunnel):
```bash
python -m app.webhook_server
```

Validate before a real call:
```bash
python -m app.preflight --scenario call_05_weekend_request --real-call
```

Place a real call (requires typing the confirmation phrase `CALL_ASSESSMENT_LINE`):
```bash
python -m app.call_runner --scenario call_05_weekend_request --real-call
```

Generate final artifacts after calls complete:
```bash
python -m app.prepare_final_artifacts
```

## Project Structure

```
app/          Core application code (call orchestration, webhook server, artifact prep)
calls/        Generated local and Twilio call outputs
docs/         Architecture and setup notes
final_calls/  Final selected call artifacts (recording, transcript, metadata, notes per scenario)
reports/      Bug report and evaluation notes
tests/        Test files
```

## Tech Stack

Python, Twilio (voice + webhooks), Flask, speech-to-text/text-to-speech APIs
