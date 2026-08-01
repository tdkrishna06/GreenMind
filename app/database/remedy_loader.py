import json

with open("app/database/remedies.json", "r", encoding="utf-8") as file:
    REMEDIES = json.load(file)

def normalize(name):
    return (
        name.lower()
        .replace("___", " ")
        .replace("__", " ")
        .replace("_", " ")
        .replace("(", "")
        .replace(")", "")
        .strip()
    )

def get_remedy(disease_name):

    normalized = normalize(disease_name)

    for key, value in REMEDIES.items():
        if normalize(key) == normalized:
            return value

    return None