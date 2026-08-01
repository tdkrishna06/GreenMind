"""Small local JSON diagnosis history store."""
from __future__ import annotations
from datetime import datetime, timezone
import json
from configs.settings import DATA_DIR, HISTORY_FILE


def append(record: dict) -> None:
    """Persist one diagnosis without storing the uploaded image."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    entries = read()
    record["timestamp"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    entries.insert(0, record)
    HISTORY_FILE.write_text(json.dumps(entries[:100], indent=2), encoding="utf-8")


def read() -> list[dict]:
    """Return stored records, recovering safely from absent or malformed data."""
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []
