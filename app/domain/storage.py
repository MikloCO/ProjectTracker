# core/storage.py
import json
from pathlib import Path

import structlog

from .models import Course

DATA_FILE = Path("data/courses.json")


def save_courses(courses: list[Course]):
    """Serialize all courses to the JSON data file, creating it if needed."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    print("SAVE PATH:", DATA_FILE.resolve())

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([c.model_dump() for c in courses], f, indent=4)
    except Exception as e:
        structlog.get_logger().error("Failed to save courses", error=str(e))


def load_courses() -> list[Course]:
    """Load and validate all courses from the JSON data file, returning an empty list if it doesn't exist."""
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE) as f:
        raw = json.load(f)

    return [Course.model_validate(c) for c in raw]
