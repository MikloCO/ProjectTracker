import contextlib
import json
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    STYLES_DIR = Path(sys._MEIPASS) / "app" / "ui" / "styles"
else:
    STYLES_DIR = Path(__file__).parent / "styles"
SETTINGS_FILE = Path.home() / ".course_tracker" / "settings.json"

THEMES = ("dark", "light", "midnight")
DEFAULT_THEME = "dark"


def load_theme(name: str) -> str:
    path = STYLES_DIR / f"{name}.qss"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def get_saved_theme() -> str:
    if SETTINGS_FILE.exists():
        try:
            data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            return data.get("theme", DEFAULT_THEME)
        except Exception:
            pass
    return DEFAULT_THEME


def save_theme(name: str) -> None:
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    settings: dict = {}
    if SETTINGS_FILE.exists():
        with contextlib.suppress(Exception):
            settings = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    settings["theme"] = name
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")
