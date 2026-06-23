def fake_clinic_response(user_message: str, turn_number: int) -> str:
    """
    Simple fake clinic agent for local testing.

    This is not the final assessment agent. It only helps test scenario flow
    before connecting the project to real phone calls.
    """

    message = user_message.lower()

    if turn_number == 0:
        return "Thanks for calling. How can I help you today?"

    if "appointment" in message or "schedule" in message:
        return "I can help with scheduling. Can I have your full name and date of birth?"

    if "refill" in message or "medication" in message:
        return "I can help route that request. Which medication are you calling about?"

    if "insurance" in message:
        return "We accept several insurance plans. Which insurance provider do you have?"

    if "address" in message or "parking" in message or "location" in message:
        return "The office is located at our main clinic location. Parking details may vary, so I can help confirm that."

    if "chest" in message or "urgent" in message:
        return "If you are experiencing chest pain, chest tightness, or severe symptoms, please call 911 or seek emergency care right away."

    if "cancel" in message:
        return "I can help cancel the appointment. Can you confirm your name and appointment date?"

    if "reschedule" in message:
        return "I can help reschedule. What day would you prefer instead?"

    return "Could you tell me a little more about what you need help with?"