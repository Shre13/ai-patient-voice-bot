# AI Patient Voice Bot

A Python-based patient caller simulator for testing a healthcare voice agent.

## Current Status

- Local scenario simulation
- Fake clinic agent for offline testing
- Transcript and metadata saving
- Safety config for the assessment number
- Real phone-call integration planned later

## Safety Note

The final caller is designed to call only the assessment number provided in the challenge:

```text
+1-805-439-8008
```

The number is hard-coded in `app/config.py` instead of being accepted through user input. This reduces the risk of accidentally calling an unintended number during testing.

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.main
```

## Project Structure

```text
app/      Core Python code
calls/    Saved transcripts and call outputs
docs/     Architecture and iteration notes
reports/  Final bug reports
tests/    Tests
```

## Local Simulation

The current version runs 10 local patient scenarios against a fake clinic agent. This allows scenario flow and transcript saving to be tested before using paid telephony or voice APIs.

## Local Webhook Test

The Twilio webhook skeleton can be tested locally:

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

This currently returns placeholder TwiML only. It does not place a real phone call.

## Public Webhook URL

For real Twilio calls, the local Flask webhook must be exposed through a public HTTPS tunnel. The public base URL should be placed in `.env` as:

```env
PUBLIC_WEBHOOK_BASE_URL=