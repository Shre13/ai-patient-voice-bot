# AI Patient Voice Bot

A Python-based patient caller simulator for testing a healthcare voice agent.

## Current Status

- Local scenario simulation
- Fake clinic agent for offline testing
- Transcript and metadata saving
- Real phone-call integration planned later

## Safety Note

The final caller will be designed to call only the assessment number provided in the challenge.

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