# Tunnel Setup Notes

Twilio cannot reach `http://127.0.0.1:5000/voice` directly because that address only exists on my laptop. Before making a real call, the local Flask webhook needs to be exposed through a public HTTPS tunnel.

## Local server

Start the Flask webhook:

```bash
python -m app.webhook_server