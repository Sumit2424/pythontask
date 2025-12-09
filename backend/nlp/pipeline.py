# ================================================================
# pipeline.py - Full NLP Pipeline
#
# ✔ Task classification using ML model
# ✔ Name detection using name_ranker
# ✔ Deadline + Priority extraction using nlp_rules
# ✔ Returns complete structured task list
# ================================================================

import re
from mlmodel.task_predictor import is_task
from mlmodel.name_ranker import name_score
from nlp.nlp_rules import (
    extract_deadline,
    extract_priority,
    split_into_sentences
)

TASK_VERBS = [
    "fix", "update", "design", "write", "optimize",
    "improve", "build", "implement", "create",
    "develop", "deploy", "refactor", "patch"
]

# ---------------------------------------------------------------
# Step 1: Detect best name in a sentence
# ---------------------------------------------------------------
def extract_best_name(sentence: str):
    words = re.findall(r"[A-Za-z]+", sentence)
    if not words:
        return None

    scored = [(w, name_score(w)) for w in words]
    best_word, best_score = max(scored, key=lambda x: x[1])

    if best_score >= 0.4:
        return best_word

    return None


# ---------------------------------------------------------------
# Step 1.5: Split multi-action sentences into task fragments
# ---------------------------------------------------------------
def split_multi_tasks(sentence: str):
    """
    Split a multi-task sentence into smaller actionable fragments.
    This fixes the issue where capital letters (e.g., 'and Mohit')
    prevented the split from happening.
    """

    # Create lowercase matching copy — DO NOT modify original sentence.
    temp = sentence.lower()

    # Insert split markers before verbs to break multi-action sequences.
    for verb in TASK_VERBS:
        temp = temp.replace(f" and {verb}", f" || {verb}")

    # Now split using the inserted markers.
    temp_parts = [p.strip() for p in temp.split("||") if p.strip()]

    # Rebuild original case fragments by aligning temp chunks back to the original sentence.
    fragments = []
    start_index = 0
    original_lower = sentence.lower()

    for part in temp_parts:
        idx = original_lower.find(part, start_index)
        if idx != -1:
            fragments.append(sentence[idx:idx + len(part)])
            start_index = idx + len(part)
        else:
            # Fallback: use lowercase part if exact match fails
            fragments.append(part)

    return fragments


# ---------------------------------------------------------------
# Step 2: Main Transcript → Tasks Pipeline
# ---------------------------------------------------------------
def process_transcript(transcript: str):
    if not transcript:
        return []

    sentences = split_into_sentences(transcript)
    tasks = []

    for sentence in sentences:
        # A. ML task classifier
        if not is_task(sentence):
            continue

        fragments = split_multi_tasks(sentence)

        for fragment in fragments:
            # B. Name detection
            assignee = extract_best_name(fragment)

            # C. Deadline detection
            deadline = extract_deadline(fragment.lower())

            # D. Priority detection
            priority = extract_priority(fragment.lower())

            # E. Final task object
            tasks.append({
                "task": fragment.strip(),
                "assigned_to": assignee,
                "deadline": deadline,
                "priority": priority
            })

    return tasks
