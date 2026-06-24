# AI Patient Voice Bot

A Python-based AI patient voice bot for testing a healthcare phone agent through automated outbound calls, Twilio webhooks, transcript capture, recording downloads, and bug reporting.

## Final Submission Summary

This project implements an automated patient caller that places outbound calls only to the approved assessment phone number. The bot follows predefined patient scenarios, interacts with the clinic voice AI, captures live transcripts, downloads Twilio call recordings, and organizes final artifacts for review.

## Final Call Artifacts

The final selected assessment calls are located in:

```text
final_calls/
```

Each scenario folder contains:

```text
recording.mp3
transcript.txt
metadata.json
notes.md
```

The project includes 10 final call scenarios:

1. `call_01_simple_scheduling`
2. `call_02_reschedule`
3. `call_03_cancel`
4. `call_04_medication_refill`
5. `call_05_weekend_request`
6. `call_06_insurance_question`
7. `call_07_location_question`
8. `call_08_unclear_request`
9. `call_09_interruption`
10. `call_10_urgent_symptom`

## Bug Report

The final bug report is available at:

```text
reports/bug_report.md
```

It documents issues found during real-call testing, including recording-disclosure handling, demo patient profile handling, webhook event logging, recording metadata capture, and an incomplete medication-refill call that required a rerun.

## Safety Note

The caller is designed to call only the assessment number provided in the challenge:

```text
+1-805-439-8008
```

The destination number is hard-coded in `app/config.py` instead of being accepted through user input. This reduces the risk of accidentally calling an unintended number during testing.

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Local Simulation

Run a local fake-clinic simulation:

```bash
python -m app.main
```

Run a specific scenario:

```bash
python -m app.main --scenario call_05_weekend_request
```

## Webhook Server

Start the Flask webhook server:

```bash
python -m app.webhook_server
```

Health check:

```text
http://127.0.0.1:5000/health
```

Voice webhook:

```text
http://127.0.0.1:5000/voice
```

## Public Webhook URL

For real Twilio calls, the local Flask webhook must be exposed through a public HTTPS tunnel. The public base URL should be placed in `.env` as:

```env
PUBLIC_WEBHOOK_BASE_URL=https://your-public-tunnel-url
```

## Preflight Checks

Run setup checks before a dry-run:

```bash
python -m app.preflight --scenario call_05_weekend_request
```

Run stricter checks before a real call:

```bash
python -m app.preflight --scenario call_05_weekend_request --real-call
```

The real-call preflight requires a valid public webhook URL in `.env`.

## Real Call Runner

Dry-run validation:

```bash
python -m app.call_runner --scenario call_05_weekend_request
```

Real call mode:

```bash
python -m app.call_runner --scenario call_05_weekend_request --real-call
```

Before placing a real call, the script requires the exact confirmation phrase:

```text
CALL_ASSESSMENT_LINE
```

## Final Artifact Preparation

After real calls complete, final call artifacts can be prepared with:

```bash
python -m app.prepare_final_artifacts
```

This script downloads Twilio recordings and creates clean `metadata.json` and `notes.md` files for each final call folder.

## Project Structure

```text
app/          Core Python application code
calls/        Generated local and Twilio call outputs
docs/         Architecture and setup notes
final_calls/  Final selected assessment artifacts
reports/      Bug report and evaluation notes
tests/        Test files
```

## Environment Variables

Create a local `.env` file based on `.env.example`.

Required for real calls:

```env
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
PUBLIC_WEBHOOK_BASE_URL=
```

The `.env` file is intentionally excluded from Git.
