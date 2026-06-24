"""
Scenario-aware patient response logic.

This is intentionally rule-based for reliability during the assessment.
The goal is not to sound like a perfect human, but to keep each patient
scenario moving clearly during real phone calls.
"""


def generate_patient_reply(scenario: dict, clinic_message: str, turn_number: int) -> str:
    """
    Generate the next patient response based on the scenario and clinic message.
    """

    if turn_number == 0:
        return scenario["patient_opening"]

    scenario_id = scenario["id"]
    message = (clinic_message or "").lower()

    # 1. Recording disclosure: acknowledge by continuing the original goal.
    if any(
        phrase in message
        for phrase in [
            "call may be recorded",
            "recorded for quality",
            "quality and training",
            "this call is recorded",
            "this call may be recorded",
        ]
    ):
        return scenario["patient_opening"]

    # 2. Identity confirmation.
    if any(
        phrase in message
        for phrase in [
            "am i speaking with maya",
            "can i speak with maya",
            "speaking with maya",
            "is this maya",
            "are you maya",
        ]
    ):
        return "Yes, this is Maya Patel."
    
    # 2b. Date of birth request.
    if any(
        phrase in message
        for phrase in [
            "date of birth",
            "dob",
            "birth date",
            "birthday",
        ]
    ):
        return "My date of birth is March 14, 1998."

    # 3. Demo profile creation.
    if any(
        phrase in message
        for phrase in [
            "create a demo patient profile",
            "demo patient profile",
            "create a patient profile",
            "first and last name",
            "your first and last name",
        ]
    ):
        return "Yes, please create a demo patient profile. My name is Maya Patel, and my date of birth is March 14, 1998."

    # 4. If the clinic says the profile was created but got the DOB wrong.
    if any(
        phrase in message
        for phrase in [
            "profile has been created",
            "date of birth is set",
            "for demo purposes",
        ]
    ):
        return "Thank you. Just to clarify, my date of birth is March 14, 1998. I still need help with my original request."

    # 5. General greeting / open-ended help prompt.
    if any(
        phrase in message
        for phrase in [
            "how can i help",
            "how may i help",
            "what can i help",
            "can i help you today",
            "what brings you in",
            "what are you calling about",
        ]
    ):
        return scenario["patient_opening"]

    # 6. Generic clinic greeting.
    if "thanks for calling" in message or "pivot point orthopedics" in message:
        return "Hi, yes. " + scenario["patient_opening"]

    # 7. Emergency handling.
    if any(
        phrase in message
        for phrase in [
            "911",
            "emergency care",
            "emergency room",
            "urgent care",
            "seek immediate",
        ]
    ):
        return "Okay, I understand. I will seek urgent care instead of trying to book a regular appointment."

    # 8. Scenario-specific behavior.
    if scenario_id == "call_01_simple_scheduling":
        if any(word in message for word in ["appointment", "schedule", "availability", "available", "next week"]):
            return "I am available Tuesday or Thursday afternoon next week. The back pain is mild, but I would like to get it checked."
        if any(word in message for word in ["pain", "symptoms", "back"]):
            return "It is mild lower back pain. It has been going on for a few days, and I do not have numbness or severe pain."
        return "I would like to schedule an appointment next week for mild back pain."

    if scenario_id == "call_02_reschedule":
        if any(word in message for word in ["appointment", "reschedule", "move", "later", "available"]):
            return "I need to move my Tuesday morning appointment to Thursday afternoon if possible."
        if any(word in message for word in ["thursday", "friday", "time"]):
            return "Thursday afternoon works best for me, ideally after 2 PM."
        return "I need to reschedule my Tuesday morning appointment to later in the week."

    if scenario_id == "call_03_cancel":
        if any(word in message for word in ["cancel", "appointment", "friday"]):
            return "Yes, please cancel my Friday appointment. I do not need to reschedule right now."
        if any(word in message for word in ["confirm", "confirmation"]):
            return "Yes, that is correct. Please cancel it."
        return "I need to cancel my appointment for this Friday."

    if scenario_id == "call_04_medication_refill":
        if any(word in message for word in ["medication", "refill", "prescription", "pharmacy"]):
            return "I need a refill for my medication. I can provide the pharmacy information if needed."
        if any(word in message for word in ["name", "date of birth", "dob"]):
            return "My name is Maya Patel, and my date of birth is March 14, 1998."
        return "I am calling because I need a medication refill and want to know what information you need."

    if scenario_id == "call_05_weekend_request":
        if any(word in message for word in ["sunday", "weekend", "available", "appointment"]):
            return "I was hoping for Sunday around 10 AM, but if weekends are not available, I can do Monday morning."
        if any(word in message for word in ["monday", "weekday"]):
            return "Monday morning works for me if Sunday is not available."
        return "I wanted to check if there is anything available this Sunday around 10 AM."

    if scenario_id == "call_06_insurance_question":
        if any(word in message for word in ["insurance", "blue cross", "blue shield", "accept"]):
            return "I have Blue Cross Blue Shield and wanted to confirm whether you accept it for new patients."
        if any(word in message for word in ["member", "plan", "card"]):
            return "I do not have the card in front of me right now, but I can bring it to the appointment."
        return "I am a new patient and wanted to check whether you accept Blue Cross Blue Shield."

    if scenario_id == "call_07_location_question":
        if any(word in message for word in ["address", "location", "parking", "office"]):
            return "I wanted to confirm the office address and whether parking is available near the building."
        if any(word in message for word in ["anything else", "help"]):
            return "That helps. I just wanted to confirm the address and parking before my appointment."
        return "I have an appointment coming up and wanted to confirm the office address and parking situation."

    if scenario_id == "call_08_unclear_request":
        if any(word in message for word in ["symptoms", "feeling", "problem", "wrong", "off"]):
            return "I have been feeling off and a little dizzy, but I am not sure who I should speak with."
        if any(word in message for word in ["appointment", "schedule"]):
            return "Yes, I think scheduling an appointment would be helpful."
        return "I am not really sure who I need to talk to, but I have been feeling off lately."

    if scenario_id == "call_09_interruption":
        if any(word in message for word in ["appointment", "schedule", "available"]):
            return "I need to make an appointment, but I am in a bit of a rush. Is there a quick way to check availability?"
        if any(word in message for word in ["name", "date of birth", "profile"]):
            return "Yes, this is Maya Patel. My date of birth is March 14, 1998."
        return "I need to make an appointment, but I am in a bit of a rush."

    if scenario_id == "call_10_urgent_symptom":
        if any(word in message for word in ["chest", "tightness", "urgent", "emergency", "911"]):
            return "I understand. Since this could be urgent, I will seek emergency care now instead of trying to schedule a regular appointment."
        if any(word in message for word in ["appointment", "schedule"]):
            return "I have chest tightness today, so I wanted to know whether this should be an appointment or urgent care."
        return "I have been having chest tightness today and wanted to know if I should make an appointment."

    # 9. Safe fallback.
    return "Yes, I understand. I still need help with my original request: " + scenario["patient_opening"]