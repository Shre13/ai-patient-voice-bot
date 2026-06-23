# Final Call Artifacts

This folder is reserved for the final selected assessment calls.

Local development runs are saved under `calls/` and ignored by Git. Final reviewed calls should be copied here before submission.

Each final call folder should include:

```text
recording.mp3 or recording.ogg
transcript.txt
metadata.json
notes.md

## Tunnel Setup

For real Twilio calls, the local Flask webhook must be exposed through a public HTTPS tunnel.

Start the local webhook:

```bash
python -m app.webhook_server
```

Then expose port 5000 using a tunnel tool such as ngrok:

```bash
ngrok http 5000
```

Add the public base URL to `.env`:

```env
PUBLIC_WEBHOOK_BASE_URL=
```

Do not include `/voice`; the app appends webhook paths automatically.