def fake_clinic_response(user_message: str, turn_number: int) -> str:
    """
    Simple fake clinic agent for local testing.

    This is not the final assessment agent. It only helps test scenario flow
    before connecting the project to real phone calls.
    """

    message = user_message.lower()

    if turn_number == 0:
        return "Thanks for calling. How can I help you today?"

    if "chest tightness" in message or "chest pain" in message:
        return "If you are having chest tightness or chest pain today, please call 911 or seek emergency care right away."

    if "yes, please cancel" in message or "just need to cancel" in message:
        return "I can help cancel the appointment. I will mark the Friday appointment as canceled."

    if "refill" in message or "medication" in message or "metformin" in message:
        if "metformin" in message:
            return "Thanks. I can send a refill request to the care team. Are you completely out of the medication?"
        return "I can help route that request. Which medication are you calling about?"

    if "blue cross" in message or "insurance" in message:
        return "We can check insurance before scheduling. I would recommend confirming your plan details with the front desk."

    if "address" in message or "parking" in message or "location" in message:
        return "I can help with that. The office address and parking details should be confirmed before your appointment."

    if "cancel" in message:
        return "I can help cancel the appointment. Can you confirm your full name and date of birth?"

    if "reschedule" in message:
        return "I can help reschedule. Can you confirm your full name and date of birth first?"

    if "sunday" in message:
        return "I would need to check whether weekend appointments are available before confirming that."

    if "appointment" in message or "schedule" in message:
        return "I can help with scheduling. Can I have your full name and date of birth?"

    if "maya patel" in message or "march 14" in message:
        return "Thank you. What day or time would work best for you?"

    if "thursday afternoon" in message:
        return "Thursday afternoon may work. I would confirm the exact availability before booking."

    if "ran out" in message:
        return "I understand. For medication questions, I can route this to the care team, but I cannot give medical advice."

    if "thank you" in message:
        return "You're welcome. Have a good day."

    return "Could you share one more detail so I can route you correctly?"