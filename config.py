import os
import logging
import json
from pathlib import Path

if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

CREW_CHAT_ID = os.getenv("CREW_CHAT_ID")

ITEMS_FILE = Path(__file__).parent / "assets" / "items.json"

def get_refill_options() -> dict:
    if not ITEMS_FILE.exists():
        return {}
    try:
        with open(ITEMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding {ITEMS_FILE}: {e}")
        return {}

FAQ_FILE = Path(__file__).parent / "assets" / "faq.json"

def get_faq_data() -> list:
    if not FAQ_FILE.exists():
        return []
    try:
        with open(FAQ_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("questions", [])
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding {FAQ_FILE}: {e}")
        return []

def setup_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)