from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import texts

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=texts.START_MESSAGE.format(name=name)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(texts.HELP_MESSAGE)

handlers = [
    CommandHandler("start", start_command),
    CommandHandler("help", help_command),
]