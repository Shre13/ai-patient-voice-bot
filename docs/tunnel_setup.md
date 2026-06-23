# Tunnel Setup Notes

Twilio cannot call a local URL like:

```text
http://127.0.0.1:5000/voice
```

because that address only exists on my laptop. For real Twilio calls, I need to expose the local Flask webhook through a public HTTPS tunnel.

## Start local webhook server

```bash
python -m app.webhook_server
```

Local endpoints:

```text
http://127.0.0.1:5000/health
http://127.0.0.1:5000/voice
```

## Start public tunnel

Use ngrok or another tunnel provider to expose port 5000.

Example:

```bash
ngrok http 5000
```

Example public URL:

```text
https://example-tunnel-url.ngrok-free.app
```

## Add public URL to `.env`

Do not include `/voice`.

Correct:

```env
PUBLIC_WEBHOOK_BASE_URL=https://example-tunnel-url.ngrok-free.app
```

Incorrect:

```env
PUBLIC_WEBHOOK_BASE_URL=https://example-tunnel-url.ngrok-free.app/voice
```

The app automatically appends `/voice`, `/status-callback`, and `/recording-callback`.

## Pre-call checklist

Before making a real call:

- [ ] Flask server is running
- [ ] Public tunnel is running
- [ ] `/health` works through the public tunnel
- [ ] `/voice` returns TwiML through the public tunnel
- [ ] `PUBLIC_WEBHOOK_BASE_URL` is set in `.env`
- [ ] Twilio credentials are set in `.env`
- [ ] Twilio phone number is set in `.env`
- [ ] Real-call confirmation guard is still enabled
- [ ] Assessment number safety guard is still enabled