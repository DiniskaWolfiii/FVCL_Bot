"""Configuration module for FVCL_Bot.

Loads environment variables, configures timezones and logging,
and provides helper functions to read static JSON assets.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from zoneinfo import ZoneInfo

# Manually load .env file if present
_ENV_PATH = Path(".env")
if _ENV_PATH.exists():
    with open(_ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

# Bot Token
BOT_TOKEN: Optional[str] = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

# Crew Chat ID (parsed as integer if numerical)
_raw_crew_chat_id = os.getenv("CREW_CHAT_ID")
CREW_CHAT_ID: Optional[int] = None
if _raw_crew_chat_id:
    try:
        CREW_CHAT_ID = int(_raw_crew_chat_id.strip())
    except ValueError:
        logging.warning("CREW_CHAT_ID is not a valid integer: %s", _raw_crew_chat_id)

# Timezone (Default: Europe/Berlin)
TIMEZONE: ZoneInfo = ZoneInfo(os.getenv("BOT_TIMEZONE", "Europe/Berlin"))

# Action cooldowns in seconds (Anti-spam protection)
ACTION_COOLDOWN_SECONDS: int = int(os.getenv("ACTION_COOLDOWN_SECONDS", "15"))

# File paths for static assets
_ASSETS_DIR = Path(__file__).parent / "assets"
ITEMS_FILE: Path = _ASSETS_DIR / "items.json"
FAQ_FILE: Path = _ASSETS_DIR / "faq.json"
OPENING_FILE: Path = _ASSETS_DIR / "opening.json"


def get_refill_options() -> Dict[str, str]:
    """Loads available refill items from items.json."""
    if not ITEMS_FILE.exists():
        logging.warning("File %s does not exist.", ITEMS_FILE)
        return {}
    try:
        with open(ITEMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logging.error("Error loading %s: %s", ITEMS_FILE, e)
        return {}


def get_faq_data() -> List[Dict[str, str]]:
    """Loads FAQ questions and answers from faq.json."""
    if not FAQ_FILE.exists():
        logging.warning("File %s does not exist.", FAQ_FILE)
        return []
    try:
        with open(FAQ_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("questions", [])
    except (json.JSONDecodeError, OSError) as e:
        logging.error("Error loading %s: %s", FAQ_FILE, e)
        return []


def get_opening_data() -> Dict[str, Dict[str, str]]:
    """Loads lounge operating hours from opening.json."""
    if not OPENING_FILE.exists():
        logging.warning("File %s does not exist.", OPENING_FILE)
        return {}
    try:
        with open(OPENING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logging.error("Error loading %s: %s", OPENING_FILE, e)
        return {}


def setup_logging() -> None:
    """Configures application logging for the bot."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)