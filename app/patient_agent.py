def generate_patient_reply(scenario: dict, clinic_message: str, turn_number: int) -> str:
    """
    Local rule-based patient bot.

    Later, this can be replaced with an LLM-backed patient agent.
    Keeping the first version simple makes it easier to test scenario flow.
    """

    if turn_number == 0:
        return scenario["patient_opening"]

    scenario_id = scenario["id"]
    clinic_message_lower = clinic_message.lower()

    if any(
        phrase in clinic_message_lower
        for phrase in [
            "call may be recorded",
            "recorded for quality",
            "quality and training",
            "this call is recorded",
        ]
    ):
        return scenario["patient_opening"]
    
    if "demo patient profile" in clinic_message_lower or "create a demo patient" in clinic_message_lower:
        return "Yes, please create a demo patient profile. My name is Maya Patel and my date of birth is March 14, 1998."

    if "911" in clinic_message_lower or "emergency care" in clinic_message_lower:
        return "Okay, I understand. I will seek urgent care instead of trying to book a regular appointment."

    if "weekend appointments" in clinic_message_lower:
        return "Okay, if Sunday is not available, I can try a weekday instead. Thank you for your help."

    if "plan details" in clinic_message_lower or "front desk" in clinic_message_lower:
        return "That makes sense. I will confirm my plan details with the front desk. Thank you for your help."

    if "office address" in clinic_message_lower or "parking details" in clinic_message_lower:
        return "Okay, I will confirm the exact address and parking details before coming in. Thank you for your help."

    if "completely out" in clinic_message_lower:
        return "Yes, I am completely out. I understand you need to route it to the care team. Thank you for your help."

    if "which medication" in clinic_message_lower:
        return "It is for metformin. I ran out two days ago and wanted to know what I should do."

    if "name" in clinic_message_lower or "date of birth" in clinic_message_lower:
        return "Sure, my name is Maya Patel and my date of birth is March 14, 1998."

    if "what day" in clinic_message_lower or "what day or time" in clinic_message_lower:
        if "reschedule" in scenario_id:
            return "Thursday afternoon would work better for me."
        if "cancel" in scenario_id:
            return "It is for this Friday. I just need to cancel it."
        return "Thursday afternoon would work if there is anything available."

    if "thursday afternoon" in clinic_message_lower or "exact availability" in clinic_message_lower:
        return "That works. Please confirm the exact time when available. Thank you for your help."

    if "cancel the appointment" in clinic_message_lower and turn_number >= 2:
        return "Yes, please cancel the Friday appointment. Thank you for your help."

    if "one more detail" in clinic_message_lower or "route" in clinic_message_lower:
        if "unclear" in scenario_id:
            return "I have been feeling dizzy and tired, but I am not sure if I need an appointment or just advice."
        return "I just want to make sure I am speaking with the right person."

    if turn_number >= 4:
        return "That answers my question. Thank you for your help."

    return "Okay, thank you. What would be the next step?"