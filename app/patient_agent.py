"""
Scenario-aware patient response logic.

This bot is intentionally rule-based for reliability during the assessment.
The goal is to keep each patient scenario moving clearly during real phone calls,
handle common clinic AI prompts, and avoid generic fallback responses.
"""


PATIENT_NAME = "Maya Patel"
PATIENT_DOB = "March 14, 1998"
PATIENT_PHONE = "555-0134"
PATIENT_EMAIL = "maya.patel@example.com"
PATIENT_INSURANCE = "Blue Cross Blue Shield"


def _contains(message: str, phrases: list[str]) -> bool:
    return any(phrase in message for phrase in phrases)


def _scenario_opening(scenario: dict) -> str:
    return scenario["patient_opening"]


def _identity_response() -> str:
    return f"Yes, this is {PATIENT_NAME}."


def _dob_response() -> str:
    return f"My date of birth is {PATIENT_DOB}."


def _name_and_dob_response() -> str:
    return f"My name is {PATIENT_NAME}, and my date of birth is {PATIENT_DOB}."


def _contact_response() -> str:
    return f"My phone number is {PATIENT_PHONE}, and my email is {PATIENT_EMAIL}."


def generate_patient_reply(scenario: dict, clinic_message: str, turn_number: int) -> str:
    """
    Generate the next patient response based on the scenario and clinic message.
    """

    if turn_number == 0:
        return _scenario_opening(scenario)

    scenario_id = scenario["id"]
    message = (clinic_message or "").lower()

    # ---------------------------------------------------------------------
    # Global handling: these prompts can appear in any scenario.
    # Order matters. Help prompts must come before DOB/profile mismatch logic
    # because the clinic may mention DOB and then ask how it can help.
    # ---------------------------------------------------------------------

    # Recording disclosure / Spanish prompt / automated intro.
    if _contains(
        message,
        [
            "call may be recorded",
            "recorded for quality",
            "quality and training",
            "this call is recorded",
            "this call may be recorded",
            "para español",
            "but espanol",
            "for spanish",
        ],
    ):
        return _scenario_opening(scenario)

    # Generic greeting where the clinic asks how it can help.
    if _contains(
        message,
        [
            "how can i help you today",
            "how can i help",
            "how may i help",
            "how may i assist",
            "how can i assist",
            "what can i help you with",
            "what can i help",
            "what do you need help with",
            "what are you calling about",
            "what brings you in",
            "how may i direct your call",
            "how can we help",
        ],
    ):
        return _scenario_opening(scenario)

    # Identity confirmation.
    if _contains(
        message,
        [
            "am i speaking with maya",
            "can i speak with maya",
            "speaking with maya",
            "is this maya",
            "are you maya",
            "is this maya patel",
            "maya patel",
        ],
    ):
        return _identity_response()

    # First/last name request.
    if _contains(
        message,
        [
            "first and last name",
            "your first and last name",
            "can i have your name",
            "may i have your name",
            "what is your name",
            "what's your name",
            "full name",
        ],
    ):
        return f"My name is {PATIENT_NAME}."

    # Strict DOB request. Keep this strict to avoid repeated DOB responses when
    # the clinic says "I have your date of birth..." or "birthday doesn't match..."
    if _contains(
        message,
        [
            "please provide your date of birth",
            "provide your date of birth",
            "what is your date of birth",
            "what's your date of birth",
            "can i have your date of birth",
            "may i have your date of birth",
            "could i have your date of birth",
            "please provide your dob",
            "provide your dob",
            "what is your dob",
            "what's your dob",
            "date of birth please",
            "dob please",
            "birthday please",
        ],
    ):
        return _dob_response()

    # Phone/email/contact request.
    if _contains(
        message,
        [
            "phone number",
            "best phone",
            "callback number",
            "call back number",
            "email address",
            "contact information",
            "best way to reach you",
        ],
    ):
        return _contact_response()

    # Demo profile creation.
    if _contains(
        message,
        [
            "create a demo patient profile",
            "demo patient profile",
            "create a patient profile",
            "set up a profile",
            "make a profile",
            "new patient profile",
        ],
    ):
        return (
            f"Yes, please create a demo patient profile. "
            f"My name is {PATIENT_NAME}, and my date of birth is {PATIENT_DOB}."
        )

    # DOB/profile mismatch or accepted profile. Continue the original goal.
    if _contains(
        message,
        [
            "profile has been created",
            "date of birth is set",
            "for demo purposes",
            "i'll accept it",
            "i will accept it",
            "doesn't match our records",
            "does not match our records",
            "i have your date of birth",
            "birthday doesn't match",
            "birthday does not match",
            "noted",
        ],
    ):
        return _scenario_opening(scenario)

    # Generic clinic intro without a direct question.
    if _contains(
        message,
        [
            "thanks for calling",
            "thank you for calling",
            "pivot point orthopedics",
            "pretty good ai",
        ],
    ):
        return "Hi, yes. " + _scenario_opening(scenario)

    # Emergency instructions. This should override normal scheduling.
    if _contains(
        message,
        [
            "call 911",
            "dial 911",
            "emergency room",
            "emergency care",
            "seek emergency",
            "seek immediate",
            "medical emergency",
            "urgent care now",
        ],
    ):
        return (
            "Okay, I understand. I will seek emergency care now instead of "
            "trying to book a regular appointment."
        )

    # If the clinic says it is transferring or placing on hold.
    if _contains(
        message,
        [
            "please hold",
            "place you on hold",
            "transfer you",
            "connect you",
            "one moment",
        ],
    ):
        return "Okay, I can hold for a moment."

    # Confirmation / wrap-up prompts.
    if _contains(
        message,
        [
            "is that correct",
            "does that sound right",
            "anything else",
            "is there anything else",
            "did i answer your question",
            "does that help",
        ],
    ):
        return "Yes, that sounds right. That answers my question."

    # ---------------------------------------------------------------------
    # Scenario-specific behavior.
    # ---------------------------------------------------------------------

    if scenario_id == "call_01_simple_scheduling":
        if _contains(message, ["symptom", "pain", "back", "reason for visit"]):
            return (
                "It is mild lower back pain. It has been going on for a few days. "
                "I do not have numbness, weakness, or severe pain."
            )

        if _contains(message, ["available", "availability", "appointment", "schedule", "openings", "time", "date"]):
            return (
                "I am available Tuesday or Thursday afternoon next week. "
                "I would prefer Thursday afternoon if possible."
            )

        if _contains(message, ["new patient", "existing patient", "seen us before"]):
            return "I am a new patient."

        if _contains(message, ["confirm", "book", "scheduled"]):
            return "Yes, please book that appointment. Thank you."

        return (
            "I would like to schedule an appointment next week for mild back pain. "
            "Thursday afternoon would work best."
        )

    if scenario_id == "call_02_reschedule":
        if _contains(message, ["which appointment", "current appointment", "when is your appointment"]):
            return "My current appointment is Tuesday morning."

        if _contains(message, ["available", "availability", "reschedule", "move", "later", "time", "date", "appointment"]):
            return "I need to move my Tuesday morning appointment to Thursday afternoon if possible."

        if _contains(message, ["thursday", "friday", "afternoon", "morning"]):
            return "Thursday afternoon works best for me, ideally after 2 PM."

        if _contains(message, ["cancel", "remove original", "old appointment"]):
            return "Yes, please move the Tuesday appointment to the new Thursday afternoon time."

        if _contains(message, ["confirm", "scheduled", "changed"]):
            return "Yes, that works. Thank you for rescheduling it."

        return "I need to reschedule my Tuesday morning appointment to later in the week."

    if scenario_id == "call_03_cancel":
        if _contains(message, ["which appointment", "what appointment", "when is your appointment"]):
            return "It is my appointment this Friday."

        if _contains(message, ["cancel", "appointment", "friday"]):
            return "Yes, please cancel my Friday appointment. I do not need to reschedule right now."

        if _contains(message, ["reschedule", "new appointment", "another time"]):
            return "No, I do not need to reschedule right now. I only want to cancel it."

        if _contains(message, ["confirm", "cancelled", "canceled"]):
            return "Yes, that is correct. Please cancel it."

        return "I need to cancel my appointment for this Friday."

    if scenario_id == "call_04_medication_refill":
        if _contains(message, ["which medication", "medication name", "what medication"]):
            return "It is for my medication refill. I can confirm the exact prescription with the pharmacy if needed."

        if _contains(message, ["refill", "prescription", "medication", "pharmacy"]):
            return "I need a medication refill and can provide the pharmacy information if needed."

        if _contains(message, ["pharmacy name", "which pharmacy", "preferred pharmacy"]):
            return "My preferred pharmacy is CVS on Main Street."

        if _contains(message, ["urgent", "out of medication", "ran out"]):
            return "I am almost out of the medication, so I wanted to request the refill as soon as possible."

        if _contains(message, ["message", "provider", "doctor", "send a request"]):
            return "Yes, please send a refill request to the provider."

        if _contains(message, ["confirm", "submitted", "request sent"]):
            return "That sounds good. Thank you for submitting the refill request."

        return "I am calling because I need a medication refill and want to know what information you need."

    if scenario_id == "call_05_weekend_request":
        if _contains(message, ["sunday", "weekend", "saturday"]):
            return "I was hoping for Sunday around 10 AM."

        if _contains(message, ["not available", "no weekend", "weekday", "monday"]):
            return "If weekends are not available, Monday morning would work for me."

        if _contains(message, ["available", "availability", "appointment", "schedule", "openings"]):
            return "Sunday around 10 AM is my first choice, but Monday morning is okay as a backup."

        if _contains(message, ["confirm", "book", "scheduled"]):
            return "Yes, that appointment works for me."

        return "I wanted to check if there is anything available this Sunday around 10 AM."

    if scenario_id == "call_06_insurance_question":
        if _contains(message, ["insurance", "blue cross", "blue shield", "accept", "plan"]):
            return "I have Blue Cross Blue Shield and wanted to confirm whether you accept it for new patients."

        if _contains(message, ["member id", "member number", "policy number", "group number", "card"]):
            return "I do not have the card in front of me right now, but I can bring it to the appointment."

        if _contains(message, ["new patient", "appointment", "schedule"]):
            return "Yes, I am a new patient. I wanted to confirm insurance before scheduling."

        if _contains(message, ["verify", "billing", "coverage"]):
            return "That makes sense. I just wanted to know whether Blue Cross Blue Shield is generally accepted."

        return "I am a new patient and wanted to check whether you accept Blue Cross Blue Shield."

    if scenario_id == "call_07_location_question":
        if _contains(message, ["address", "location", "where are you", "office"]):
            return "I wanted to confirm the office address for my upcoming appointment."

        if _contains(message, ["parking", "garage", "lot", "street parking"]):
            return "I also wanted to know whether parking is available near the building."

        if _contains(message, ["appointment", "upcoming visit"]):
            return "Yes, I have an appointment coming up and wanted to confirm the address and parking."

        if _contains(message, ["anything else", "help", "directions"]):
            return "That helps. I just wanted to confirm the address and parking before my appointment."

        return "I have an appointment coming up and wanted to confirm the office address and parking situation."

    if scenario_id == "call_08_unclear_request":
        if _contains(message, ["what symptoms", "symptoms", "feeling", "problem", "wrong", "off"]):
            return "I have been feeling off and a little dizzy, but I am not sure who I should speak with."

        if _contains(message, ["severe", "chest pain", "shortness of breath", "fainting", "emergency"]):
            return "I do not have chest pain or shortness of breath. I just feel a little dizzy and off."

        if _contains(message, ["appointment", "schedule", "provider", "doctor"]):
            return "Yes, I think scheduling an appointment would be helpful."

        if _contains(message, ["nurse", "triage", "clinical team"]):
            return "Yes, speaking with a nurse or clinical team member would be helpful."

        return "I am not really sure who I need to talk to, but I have been feeling off lately."

    if scenario_id == "call_09_interruption":
        if _contains(message, ["slow down", "repeat", "didn't catch", "did not catch"]):
            return "Sure. I need to make an appointment, but I am in a bit of a rush."

        if _contains(message, ["appointment", "schedule", "available", "availability"]):
            return "I need to make an appointment, but I am in a bit of a rush. Is there a quick way to check availability?"

        if _contains(message, ["time", "date", "when"]):
            return "The earliest available appointment would be best."

        if _contains(message, ["confirm", "book", "scheduled"]):
            return "Yes, please book it. I appreciate the quick help."

        return "I need to make an appointment, but I am in a bit of a rush."

    if scenario_id == "call_10_urgent_symptom":
        # This scenario should not push for routine scheduling if the clinic gives urgent-care advice.
        if _contains(message, ["911", "emergency", "urgent care", "er", "emergency room", "seek immediate"]):
            return (
                "I understand. Since this could be urgent, I will seek emergency care now "
                "instead of trying to schedule a regular appointment."
            )

        if _contains(message, ["chest", "tightness", "symptom", "what are you experiencing"]):
            return "I have been having chest tightness today. I wanted to know if I should make an appointment or seek urgent care."

        if _contains(message, ["shortness of breath", "severe", "radiating", "left arm", "jaw pain"]):
            return "I understand that those symptoms could be serious. I will seek urgent care now."

        if _contains(message, ["appointment", "schedule"]):
            return "Because it is chest tightness today, I wanted to know whether this should be urgent care instead."

        return "I have been having chest tightness today and wanted to know if I should make an appointment."

    # Safe fallback.
    return "Yes, I understand. I still need help with my original request: " + _scenario_opening(scenario)