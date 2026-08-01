import json
from pathlib import Path

json_path = Path(__file__).parent / "remedies.json"

with open(json_path, "r", encoding="utf-8") as file:
    REMEDIES = json.load(file)

def get_remedy(disease_name):
    return REMEDIES.get(disease_name)