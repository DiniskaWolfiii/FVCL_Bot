"""Main entry point for FVCL_Bot (Furvester Crew Lounge Bot).

Initializes the Telegram Application with rate limiting, registers
handlers, policies, and the global error handler.
"""

import sys
import os
import shutil
import logging
from pathlib import Path

# Initialize custom data directory (e.g. for Docker volume /data)
DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
if DATA_DIR.is_dir():
    custom_texts = DATA_DIR / "texts.py"
    default_texts = Path(__file__).parent / "texts.py"
    if not custom_texts.exists() and default_texts.exists():
        try:
            shutil.copyfile(default_texts, custom_texts)
            try:
                os.chmod(custom_texts, 0o666)  # Allows editing on the host without sudo
            except OSError:
                pass
            print(f"Initialized default texts.py in {DATA_DIR}")
        except OSError as e:
            print(f"Warning: Could not copy default texts.py to {DATA_DIR}: {e}")

    if custom_texts.exists():
        sys.path.insert(0, str(DATA_DIR.resolve()))

from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    Application,
    ContextTypes,
    AIORateLimiter,
)
import config
from handlers import register_handlers

logger = logging.getLogger(__name__)


async def post_init(app: Application) -> None:
    """Sets bot commands for the Telegram menu button."""
    commands = [
        BotCommand("start", "Starts the bot"),
        BotCommand("faq", "Shows FAQ & info about the Lounge"),
        BotCommand("refill", "Reports needed supplies for the Crew Lounge"),
        BotCommand("report", "Reports an incident in the Crew Lounge"),
        BotCommand("rules", "Shows the Rules of the Crew Lounge. Please read and follow them!"),
    ]
    await app.bot.set_my_commands(commands)
    logger.info("Bot command menu registered successfully.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler: catches unhandled exceptions and logs the traceback."""
    logger.error(
        "Exception occurred while handling update %s: %s",
        update,
        context.error,
        exc_info=context.error,
    )


def main() -> None:
    """Starts the bot and initializes all services."""
    config.setup_logging()

    if (DATA_DIR / "texts.py").exists():
        logger.info("Custom texts loaded from: %s", DATA_DIR / "texts.py")

    if not config.BOT_TOKEN:
        logger.critical("⚠️ Please set BOT_TOKEN in the .env file!")
        sys.exit(1)

    # Initialize Application with official Telegram rate limiter
    app = (
        ApplicationBuilder()
        .token(config.BOT_TOKEN)
        .rate_limiter(AIORateLimiter())
        .post_init(post_init)
        .build()
    )

    # Register global error handler
    app.add_error_handler(error_handler)

    # Register all handler modules
    register_handlers(app)

    logger.info("Starting bot (polling)... Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
