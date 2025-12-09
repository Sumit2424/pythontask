import pandas as pd
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(BASE_DIR, "name_dataset.csv")

INDIAN_NAMES = [
    "Aarav","Vivaan","Aditya","Vihaan","Arjun","Reyansh","Muhammad","Sai","Krishna",
    "Ishaan","Shaurya","Atharv","Ayaan","Kabir","Rudra","Dhruv","Om","Anay","Rohan",
    "Varun","Manav","Yuvraj","Harsh","Raj","Hitesh","Jignesh","Suresh","Mahesh",
    "Amit","Prakash","Rakesh","Devansh","Pranav","Siddharth","Yash","Kartik",
    "Aadhya","Ananya","Siya","Pari","Avni","Myra","Anika","Saanvi","Ira","Diya",
    "Aarohi","Aisha","Alia","Meera","Anvi","Ishita","Tanvi","Nitya","Niharika",
    "Malti","Pooja","Priya","Komal","Zara","Anita","Divya","Sneha","Kavya","Riya",
    "Shreya","Aparna","Radhika","Rekha","Manisha"
]

GLOBAL_NAMES = [
    "John","Emma","Olivia","Liam","Mia","Sophia","Noah","James","Ava","Lucas","Henry",
    "Isabella","Alexander","Daniel","Ethan","Michael","Elijah","Logan","Mason",
    "Charlotte","Emily","Amelia","Harper","Luna","Chloe","Grace","Penelope","Sofia",
    "Benjamin","Samuel","Jacob","William","Oliver","David","Matthew"
]

NON_NAMES = [
    "login", "bug", "update", "database", "performance", "design", "testing",
    "deploy", "frontend", "backend", "optimize", "api", "ui", "server",
    "screen", "feature", "task", "priority", "comment", "release"
]

def generate_new_data(n_names=400, n_non_names=400):
    dataset = []

    for _ in range(n_names):
        dataset.append([random.choice(INDIAN_NAMES + GLOBAL_NAMES), 1])

    for _ in range(n_non_names):
        dataset.append([random.choice(NON_NAMES), 0])

    random.shuffle(dataset)
    return pd.DataFrame(dataset, columns=["word", "label"])


def append_or_create():
    new_df = generate_new_data()

    if os.path.exists(output_path):
        old_df = pd.read_csv(output_path)

        combined = pd.concat([old_df, new_df], ignore_index=True)

        # Remove duplicates
        # combined.drop_duplicates(inplace=True)

        combined.to_csv(output_path, index=False)

        print("✔ Appended new rows.")
        print("Total rows now:", len(combined))

    else:
        new_df.to_csv(output_path, index=False)
        print("✔ Created new dataset.")
        print("Total rows:", len(new_df))


if __name__ == "__main__":
    append_or_create()
