import sys
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, Application
import config
from handlers import register_handlers

async def post_init(app: Application):
    """Setzt die Befehle für das Telegram-Menü links neben dem Eingabefeld."""
    commands = [
        BotCommand("start", "Starts the bot"),
        BotCommand("help", "Shows help & overview"),
        BotCommand("refill", "Reports needed supplies for the Crew Lounge"),
        BotCommand("report", "Reports an incident in the Crew Lounge"),
    ]
    await app.bot.set_my_commands(commands)


def main():
    config.setup_logging()

    if not config.BOT_TOKEN:
        print("⚠️ Bitte BOT_TOKEN in der .env hinterlegen!")
        sys.exit(1)

    app = ApplicationBuilder().token(config.BOT_TOKEN).post_init(post_init).build()

    # Alle Handler auf einmal registrieren
    register_handlers(app)

    print("Bot wird gestartet (Polling)... Drücke Strg+C zum Beenden.")
    app.run_polling()

if __name__ == "__main__":
    main()
