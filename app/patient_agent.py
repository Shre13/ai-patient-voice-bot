def generate_patient_reply(scenario: dict, clinic_message: str, turn_number: int) -> str:
    """
    Local rule-based patient bot.

    Later, this can be replaced with an LLM-backed patient agent.
    Keeping the first version simple makes it easier to test the scenario flow.
    """

    if turn_number == 0:
        return scenario["patient_opening"]

    goal = scenario["goal"].lower()
    clinic_message_lower = clinic_message.lower()

    if "name" in clinic_message_lower or "date of birth" in clinic_message_lower:
        return "Sure, my name is Maya Patel and my date of birth is March 14, 1998."

    if "what day" in clinic_message_lower or "prefer" in clinic_message_lower:
        if "sunday" in goal:
            return "Sunday around 10 AM would be best if you have that."
        return "Thursday afternoon would work if there is anything available."

    if "medication" in clinic_message_lower:
        return "It is for metformin. I ran out recently and wanted to know what I should do next."

    if "insurance" in clinic_message_lower or "provider" in clinic_message_lower:
        return "I have Blue Cross Blue Shield. I just wanted to confirm before booking."

    if "emergency" in clinic_message_lower or "911" in clinic_message_lower:
        return "Okay, I understand. I will seek urgent care instead of trying to book a regular appointment."

    if turn_number >= 4:
        return "That answers my question. Thank you for your help."

    return "Okay, can you help me with that?"