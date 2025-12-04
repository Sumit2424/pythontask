# ================================================================
# assignment_logic.py
#
# Responsibilities:
#   ✔ Assign tasks to team members
#   ✔ Direct assignment if name appears in the sentence
#   ✔ Skill-based assignment when no name is mentioned
#   ✔ Provide fallback "Unassigned" if no match found
#
# NOTE:
#   For now we use team_members.json to load team data.
#   Later we can add ML-based assignment for more accuracy.
# ==============================================================

import json
import os

# ---------------------------------------------------------------
# Load team member data from JSON file
# ---------------------------------------------------------------

TEAM_FILE = "backend/models/team_members.json"

if os.path.exists(TEAM_FILE):
    with open(TEAM_FILE, "r") as f:
        team_members = json.load(f)
else:
    team_members = []


# ---------------------------------------------------------------
# Main Assignment Function
# ---------------------------------------------------------------

def assign_tasks(task_list: list):
    """
    Assign extracted tasks to team members using the following rules:
    
    1️⃣ Direct Assignment:
        If NLP extracted a name → keep that assignment.
    
    2️⃣ Skill-Based Assignment:
        If no name is found, check task text for skill keywords.
    
    3️⃣ Fallback:
        If no skills match → assign as 'Unassigned'
    
    Args:
        task_list (list): Output from NLP (tasks with partial info)
    
    Returns:
        list: Tasks with assigned team members.
    """

    for task in task_list:
        # 1️⃣ Direct assignment already found?
        if task["assigned_to"]:
            continue

        task_text = task["task"].lower()
        best_match = None
        highest_score = 0

        # ------------------------------------------
        # 2️⃣ Skill-based assignment
        # ------------------------------------------
        for member in team_members:
            score = 0

            for skill in member.get("skills", []):
                if skill.lower() in task_text:
                    score += 1

            if score > highest_score:
                highest_score = score
                best_match = member

        # ------------------------------------------
        # 3️⃣ Fallback assignment
        # ------------------------------------------
        task["assigned_to"] = best_match if best_match else "Unassigned"

    return task_list
