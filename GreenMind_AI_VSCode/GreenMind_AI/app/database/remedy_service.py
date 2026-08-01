"""Sustainable remedy and disease-information knowledge service."""
from __future__ import annotations
import json
from pathlib import Path

KNOWLEDGE_FILE = Path(__file__).with_name("remedies.json")


def prettify(label: str) -> str:
    return label.replace("___", " — ").replace("_", " ").replace("  ", " ").strip()


def get_remedy(label: str) -> dict:
    """Return disease facts and safe, organic-first recommendations."""
    records = json.loads(KNOWLEDGE_FILE.read_text(encoding="utf-8"))
    name = prettify(label)
    crop, disease = (name.split(" — ", 1) + ["Plant disease"])[:2] if " — " in name else ("Plant", name)
    is_healthy = disease.lower() == "healthy"
    default = records["healthy" if is_healthy else "disease"]
    specific = records.get(label, {})
    return {
        "plant": crop.replace("(including sour)", "").strip(),
        "scientific_name": specific.get("scientific_name", "Consult a local agronomist for cultivar-specific identification."),
        "description": specific.get("description", default["description"].format(disease=disease)),
        "severity": specific.get("severity", default["severity"]),
        "symptoms": specific.get("symptoms", default["symptoms"]),
        "cause": specific.get("cause", default["cause"]),
        "affected_parts": "Leaves; inspect stems and fruit as well.",
        "traditional_remedy": specific.get("traditional_remedy", default["traditional_remedy"]),
        "organic_remedy": default["organic_remedy"],
        "application": default["application"],
        "prevention": default["prevention"],
        "note": "Recommendations are supportive guidance. Confirm severe or fast-spreading cases with a local agricultural extension officer."
    }
