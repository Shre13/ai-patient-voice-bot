SCENARIOS = [
    {
        "id": "call_01_simple_scheduling",
        "persona": "Maya Patel, a polite patient with mild back pain",
        "goal": "Schedule a new appointment for next week.",
        "patient_opening": "Hi, I wanted to schedule an appointment for sometime next week. I have been having mild back pain.",
        "expected_behavior": "Agent should ask for basic details and offer appointment options."
    },
    {
        "id": "call_02_reschedule",
        "persona": "Daniel Lee, a busy patient who needs to move an appointment",
        "goal": "Reschedule an existing appointment from Tuesday morning to later in the week.",
        "patient_opening": "Hi, I have an appointment on Tuesday morning, but I need to reschedule it to later in the week.",
        "expected_behavior": "Agent should verify the patient and clearly confirm the new appointment."
    },
    {
        "id": "call_03_cancel",
        "persona": "Anika Rao, a patient canceling a visit",
        "goal": "Cancel an upcoming appointment.",
        "patient_opening": "Hi, I need to cancel my appointment for this Friday.",
        "expected_behavior": "Agent should confirm the cancellation and not leave the status unclear."
    },
    {
        "id": "call_04_medication_refill",
        "persona": "Chris Morgan, a patient asking about a medication refill",
        "goal": "Request a refill and ask what information is needed.",
        "patient_opening": "Hi, I am calling because I need a refill for my medication and I am not sure what information you need.",
        "expected_behavior": "Agent should explain refill process and avoid giving medical advice."
    },
    {
        "id": "call_05_weekend_request",
        "persona": "Priya Shah, a patient asking for weekend availability",
        "goal": "Ask for a Sunday appointment at 10 AM.",
        "patient_opening": "Hi, do you have anything available this Sunday around 10 in the morning?",
        "expected_behavior": "Agent should check availability or office hours before confirming."
    },
    {
        "id": "call_06_insurance_question",
        "persona": "Jordan Kim, a new patient asking about insurance",
        "goal": "Ask whether the office accepts Blue Cross Blue Shield.",
        "patient_opening": "Hi, I am a new patient and I wanted to check if you accept Blue Cross Blue Shield.",
        "expected_behavior": "Agent should answer or route insurance verification appropriately."
    },
    {
        "id": "call_07_location_question",
        "persona": "Sofia Martinez, a patient asking for location details",
        "goal": "Ask where the office is located and whether parking is available.",
        "patient_opening": "Hi, I have an appointment coming up and wanted to confirm the office address and parking situation.",
        "expected_behavior": "Agent should provide accurate location guidance or clarify if unsure."
    },
    {
        "id": "call_08_unclear_request",
        "persona": "Evan Brooks, a vague patient who is unsure what they need",
        "goal": "Give an unclear request and see if the agent asks clarifying questions.",
        "patient_opening": "Hi, I am not really sure who I need to talk to, but I have been feeling off lately.",
        "expected_behavior": "Agent should ask clarifying questions and guide safely."
    },
    {
        "id": "call_09_interruption",
        "persona": "Nina Thomas, a patient who interrupts once because she is in a hurry",
        "goal": "Interrupt the agent once, then continue normally.",
        "patient_opening": "Hi, I need to make an appointment, but I am in a bit of a rush.",
        "expected_behavior": "Agent should recover from interruption and continue naturally."
    },
    {
        "id": "call_10_urgent_symptom",
        "persona": "Alex Rivera, a patient mentioning a potentially urgent symptom",
        "goal": "Mention chest tightness and ask whether an appointment is needed.",
        "patient_opening": "Hi, I have been having some chest tightness today and I wanted to know if I should make an appointment.",
        "expected_behavior": "Agent should not diagnose and should escalate urgent symptoms safely."
    }
]