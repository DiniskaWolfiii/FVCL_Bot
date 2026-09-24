"""Main entry point for FVCL_Bot (Furvester Crew Lounge Bot).

Initializes the Telegram Application with rate limiting, registers
handlers, policies, and the global error handler.
"""

import sys
import logging
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
