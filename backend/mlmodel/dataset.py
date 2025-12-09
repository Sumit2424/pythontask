# ===================================================================
# Improved dataset.py (overwrite version)
# Generates synthetic dataset for task classification
# Output: backend/mlmodel/custom_500.csv
# ===================================================================

import os
import random
import pandas as pd

# Ensure correct folder exists
os.makedirs("backend/mlmodel", exist_ok=True)

# ---------------------------------------------------------
# ACTION VERBS & OBJECTS (Tasks)
# ---------------------------------------------------------
ACTION_VERBS = [
    "Fix", "Update", "Optimize", "Implement", "Design", "Develop",
    "Create", "Build", "Improve", "Write", "Add", "Refactor",
    "Integrate", "Configure", "Migrate", "Resolve", "Patch",
    "Enhance", "Debug"
]

ACTION_OBJECTS = [
    "the login bug", "API documentation", "database performance", 
    "user authentication", "onboarding screen", "unit tests",
    "the recommendation engine", "the UI components",
    "the payment gateway", "the notification service",
    "the caching layer", "the monitoring dashboard",
    "the analytics API", "session management",
    "the search indexing logic", "the mobile layout",
    "logging system", "data migration script"
]

ACTION_EXTRAS = [
    "", " urgently", " by tomorrow", " by Friday", 
    " before next release", " as soon as possible",
    " for the next sprint", " due this week"
]

TASK_VARIANTS = [
    "{} {}{}", 
    "Please {} {}{}",
    "Can someone {} {}{}?",
    "We should {} {}{}",
    "We need to {} {}{}",
    "Let's {} {}{}",
    "{} {}{} please",
    "{} {} needs to be done{}",
    "Someone should {} {}{}",
    "It would be good to {} {}{}"
]

NON_ACTION_SENTENCES = [
    "We will revisit this topic later.",
    "There is no urgency for this item.",
    "We need more information before proceeding.",
    "Let’s wait for stakeholder feedback.",
    "This will be discussed next week.",
    "There is no blocker right now.",
    "We should analyze this further.",
    "This decision is still pending.",
    "Nothing actionable at the moment.",
    "We can postpone this to next sprint.",
    "This requires additional approval.",
    "We should collect more data first.",
    "The team is still evaluating this.",
    "We should wait for product input.",
    "This is not a priority currently.",
    "We need design approval first.",
    "This depends on future planning.",
    "We will discuss this again tomorrow.",
    "No action items were mentioned.",
    "This is still under review."
]

AMBIGUOUS_NON_TASKS = [
    "Sakshi mentioned the login bug yesterday.",
    "Mohit worked on database performance last sprint.",
    "Arjun designed the onboarding screens last month.",
    "The login bug was fixed previously.",
    "We reviewed the API documentation last week.",
    "The database performance improved yesterday.",
    "Someone updated the payment gateway earlier.",
    "The team optimized the caching layer before."
]

NOISE = ["", "uh", "um", "so", "like"]

# ---------------------------------------------------------
# Sentence Generators
# ---------------------------------------------------------
def generate_action_sentence():
    verb = random.choice(ACTION_VERBS)
    obj = random.choice(ACTION_OBJECTS)
    extra = random.choice(ACTION_EXTRAS)
    template = random.choice(TASK_VARIANTS)
    noise = random.choice(NOISE)

    sentence = template.format(verb, obj, extra)
    return f"{noise} {sentence}".strip()


def generate_non_action_sentence():
    noise = random.choice(NOISE)
    base = random.choice(NON_ACTION_SENTENCES + AMBIGUOUS_NON_TASKS)
    return f"{noise} {base}".strip()


# ---------------------------------------------------------
# Create Dataset
# ---------------------------------------------------------
def generate_dataset(n_action=900, n_non_action=600):
    data = []

    for _ in range(n_action):
        data.append([generate_action_sentence(), 1])

    for _ in range(n_non_action):
        data.append([generate_non_action_sentence(), 0])

    random.shuffle(data)
    return pd.DataFrame(data, columns=["sentence", "label"])


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    df = generate_dataset(900, 600)  # 1,500 rows recommended
    output_path = "backend/mlmodel/custom_500.csv"

    df.to_csv(output_path, index=False)

    print("✔ Improved dataset generated!")
    print(f"✔ Saved to: {output_path}")
    print(f"✔ Total samples: {len(df)}")
