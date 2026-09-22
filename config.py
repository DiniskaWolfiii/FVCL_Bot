import os
import logging

if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

CREW_CHAT_ID = os.getenv("CREW_CHAT_ID")

REFILL_OPTIONS = {
    "refill_dildos": "Sex Toys",
    "refill_condoms": "Condoms",
    "refill_lube": "32.000oz Lube"
}

def setup_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)