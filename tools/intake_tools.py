"""
intake_tools.py: Custom tools for the Strands Patient Intake Summarization demo.

Each function decorated with @tool becomes a callable capability that
an Agent can invoke autonomously when it decides the tool is needed.

The @tool decorator:
  • Reads the function signature to auto-generate a JSON schema
  • Uses the docstring as the tool description shown to the model
  • Wraps the return value so Strands can pass it back to the agent
"""

import json
from strands import tool


# ---------------------------------------------------------------------------
# Tool 1 — Intake Parser
# ---------------------------------------------------------------------------

@tool
def parse_intake_form(
    patient_name: str,
    age: int,
    chief_complaint: str,
    symptom_duration: str,
    current_medications: str,
    allergies: str,
    relevant_history: str,
) -> str:
    """
    Parse and structure raw patient intake form responses.

    Checks that required fields are present and meaningful.
    Returns a JSON string with status 'parsed' or 'error' plus structured data.
    """
    issues = []

    if not patient_name or patient_name.strip() == "":
        issues.append("Patient name is missing.")
    if not chief_complaint or chief_complaint.strip() == "":
        issues.append("Chief complaint is missing.")
    if age <= 0 or age > 120:
        issues.append("Age must be a valid number between 1 and 120.")

    if issues:
        return json.dumps(
            {"status": "error", "issues": issues},
            indent=2,
        )

    return json.dumps(
        {
            "status": "parsed",
            "patient_name": patient_name,
            "age": age,
            "chief_complaint": chief_complaint,
            "symptom_duration": symptom_duration,
            "current_medications": current_medications,
            "allergies": allergies,
            "relevant_history": relevant_history,
        },
        indent=2,
    )


# ---------------------------------------------------------------------------
# Tool 2 — Completeness Checker
# ---------------------------------------------------------------------------

@tool
def check_completeness(
    patient_name: str,
    age: int,
    chief_complaint: str,
    symptom_duration: str,
    current_medications: str,
    allergies: str,
    relevant_history: str,
) -> str:
    """
    Check whether critical intake fields are present and meaningful.

    Critical fields: patient_name, age, chief_complaint, symptom_duration,
    current_medications, allergies, relevant_history.

    Returns a JSON string with status 'complete' or 'incomplete'
    and a list of missing or vague fields.
    """
    missing = []
    vague_markers = ["unknown", "n/a", "none", "not sure", "unsure", "not provided", "no information", "nil", "nothing", ""]

    def is_vague(value: str) -> bool:
        return not value or value.strip().lower() in vague_markers

    if is_vague(patient_name):
        missing.append("patient_name")
    if age is None or age <= 0 or age > 120:
        missing.append("age")
    if is_vague(chief_complaint):
        missing.append("chief_complaint")
    if is_vague(symptom_duration):
        missing.append("symptom_duration")
    if is_vague(current_medications):
        missing.append("current_medications")
    if is_vague(allergies):
        missing.append("allergies")
    if is_vague(relevant_history):
        missing.append("relevant_history")

    if missing:
        return json.dumps(
            {
                "status": "incomplete",
                "missing_fields": missing,
                "message": (
                    "The following critical fields are missing or vague: "
                    + ", ".join(missing)
                ),
            },
            indent=2,
        )

    return json.dumps(
        {
            "status": "complete",
            "missing_fields": [],
            "message": "All critical fields are present.",
        },
        indent=2,
    )


# ---------------------------------------------------------------------------
# Tool 3 — Symptom Organizer
# ---------------------------------------------------------------------------

@tool
def organize_symptoms(
    chief_complaint: str,
    symptom_duration: str,
    relevant_history: str,
    current_medications: str,
    allergies: str,
) -> str:
    """
    Organize and prioritize symptom information for clinical review.

    Groups information by clinical relevance and flags anything
    that may need immediate attention based on duration or history.

    Returns a JSON string with organized symptom data and
    a priority level of routine, follow_up, or urgent_review.
    """
    flags = []

    urgent_keywords = [
        "chest pain", "shortness of breath", "difficulty breathing",
        "fainting", "loss of consciousness", "severe", "sudden",
        "worst", "stroke", "seizure",
    ]
    for keyword in urgent_keywords:
        if keyword.lower() in chief_complaint.lower():
            flags.append(f"Potential urgent symptom detected: '{keyword}'")

    long_duration_markers = ["month", "year", "chronic", "ongoing", "weeks"]
    duration_note = ""
    for marker in long_duration_markers:
        if marker in symptom_duration.lower():
            duration_note = "Symptoms are ongoing or chronic, may warrant further workup."
            break

    if flags:
        priority = "urgent_review"
    elif duration_note:
        priority = "follow_up"
    else:
        priority = "routine"

    return json.dumps(
        {
            "chief_complaint": chief_complaint,
            "symptom_duration": symptom_duration,
            "duration_note": duration_note,
            "relevant_history": relevant_history,
            "current_medications": current_medications,
            "allergies": allergies,
            "flags": flags,
            "priority_level": priority,
        },
        indent=2,
    )


# ---------------------------------------------------------------------------
# Tool 4 — Clinician Summary Generator
# ---------------------------------------------------------------------------

@tool
def generate_clinician_summary(
    patient_name: str,
    age: int,
    chief_complaint: str,
    symptom_duration: str,
    current_medications: str,
    allergies: str,
    relevant_history: str,
    priority_level: str,
    flags: str,
    missing_fields: str,
    is_complete: bool,
) -> str:
    """
    Generate a structured pre-appointment clinician summary.

    If the intake is complete, produces a full summary with
    organized symptom data and suggested focus areas.
    If incomplete, produces a flagged summary listing what
    the clinician needs to collect at the start of the appointment.

    Returns a JSON string with the summary and a completeness status.
    """
    if not is_complete:
        return json.dumps(
            {
                "summary_type": "FLAGGED_INCOMPLETE",
                "patient_name": patient_name,
                "age": age,
                "chief_complaint": chief_complaint,
                "missing_fields": missing_fields,
                "note": (
                    "Intake record is incomplete. Please collect missing fields "
                    "before proceeding with clinical assessment."
                ),
            },
            indent=2,
        )

    return json.dumps(
        {
            "summary_type": "COMPLETE",
            "patient_name": patient_name,
            "age": age,
            "chief_complaint": chief_complaint,
            "symptom_duration": symptom_duration,
            "current_medications": current_medications,
            "allergies": allergies,
            "relevant_history": relevant_history,
            "priority_level": priority_level,
            "flags": flags,
            "note": "All critical fields present. Record is complete.",
        },
        indent=2,
    )
