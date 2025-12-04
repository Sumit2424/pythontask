# ================================================================
# nlp_rules.py
#
# Rule-Based NLP Logic for Task Extraction
#
# Responsibilities:
#   ✔ Identify sentences that contain actionable tasks
#   ✔ Detect the person assigned to each task
#   ✔ Extract deadlines from natural language expressions
#   ✔ Extract task priority (high, medium, low)
#   ✔ Return structured task objects to the backend
#
# This rule-based system is explainable and reliable,
# perfect for a meeting-task extraction pipeline.
# ================================================================

import re 
# ---------------------------------------------------------------
# Task Verbs – indicators that a sentence contains work/action
# ---------------------------------------------------------------

Task_VERBS = [
     "fix", "update", "design", "write", "optimize",    
    "improve", "build", "implement", "create", "develop"
]

# ---------------------------------------------------------------
# Team members (names mentioned in meeting)
# ---------------------------------------------------------------
# TODO (Future Improvement):
#   - Load team members dynamically from backend/models/team_members.json
#   - Replace static TEAM_MEMBERS list with JSON-based list
#   - Automatically detect names from transcript using NLP name-entity detection
#
# For now, using a simple static list so the system works end-to-end.


TEAM_MEMBERS = ["Sakshi", "Mohit", "Arjun", "Lata"]



# ---------------------------------------------------------------
# Deadline patterns → normalized deadline values
# ---------------------------------------------------------------
DEADLINE_PATTERNS = {
    "tomorrow evening": "Tomorrow evening",
    "tomorrow": "Tomorrow",
    "by friday": "Friday",
    "friday": "Friday",
    "next monday": "Next Monday",
    "end of this week": "End of this week",
    "this week": "This Week",
    "next week": "Next Week"
}

# ---------------------------------------------------------------
# Priority detection keywords
# ---------------------------------------------------------------
PRIORITY_MAP = {
    "critical": "High",
    "urgent": "High",
    "high priority": "High",
    "important": "High",
    "can wait": "Medium",
    "low priority": "Low"
}


# ================================================================
# MAIN FUNCTION → Extract all tasks from transcript
# ================================================================

def extract_tasks(transcript: str) -> list:
    """
     Extract actionable tasks from the transcript.

    Args:
        transcript (str): The raw meeting transcript.

    Returns:
       list of dict: Each dict contains details of a task.


    """

    if not transcript:
        return []

    sentences = split_into_sentences(transcript)
    extracted = []

    for sentence in sentences:
        lower_sentence = sentence.lower().strip()


        # -----------------------------------------------------------
        # Step 1: Check if the sentence contains a task verb
        # -----------------------------------------------------------
        if not any(verb in lower_sentence for verb in Task_VERBS):
            continue

        # -----------------------------------------------------------
        # Build Task Object
        # -----------------------------------------------------------
        task_obj = {
           "task" : sentence.strip(),
           "assigned_to":extract_assignee(sentence),
           "deadline": extract_deadline(lower_sentence),
           "priority": extract_priority(lower_sentence)
        }

        extracted.append(task_obj)

    return extracted



# ================================================================
# Helper: Extract assigned person name
# ================================================================

def extract_assignee(sentence: str):
    for member in TEAM_MEMBERS:
        if member.lower() in sentence.lower():
            return member
    return None



# ================================================================
# Helper: Extract deadlines
# ================================================================

def extract_deadline(sentence: str):
    for pattern, value in DEADLINE_PATTERNS.items():
        if pattern in sentence:
            return value
    return None



# ================================================================
# Helper: Extract priority level
# ================================================================
def extract_priority(text: str):
    for key, value in PRIORITY_MAP.items():
        if key in text:
            return value
    return None


