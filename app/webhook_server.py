from flask import Flask, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check() -> dict:
    return {"status": "ok"}


@app.route("/voice", methods=["POST", "GET"])
def voice_webhook() -> Response:
    """
    Basic Twilio voice webhook.

    This is a placeholder for the real voice-bot integration. For now, it proves
    that the app can return valid TwiML instructions to Twilio.
    """

    response = VoiceResponse()

    response.say(
        "Hello. This is the local patient bot webhook. "
        "The real voice agent integration will be connected in the next phase.",
        voice="alice",
    )

    response.pause(length=1)

    response.say(
        "This call is ending now because this is only a webhook test.",
        voice="alice",
    )

    response.hangup()

    return Response(str(response), mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
    