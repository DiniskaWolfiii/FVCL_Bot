from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
import texts
import config

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=texts.START_MESSAGE.format(name=name)
    )

def build_faq_keyboard(faq_list: list) -> InlineKeyboardMarkup:
    keyboard = []
    for i, item in enumerate(faq_list):
        keyboard.append([InlineKeyboardButton(item["question"], callback_data=f"faq_{i}")])
    return InlineKeyboardMarkup(keyboard)

async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faq_list = config.get_faq_data()
    reply_markup = build_faq_keyboard(faq_list)
    await update.effective_message.reply_text(
        text=texts.FAQ_MESSAGE,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def faq_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    faq_list = config.get_faq_data()

    if query.data == "faq_back":
        await query.edit_message_text(
            text=texts.FAQ_MESSAGE,
            reply_markup=build_faq_keyboard(faq_list),
            parse_mode="HTML"
        )
        return

    try:
        index = int(query.data.split("_")[1])
    except (IndexError, ValueError):
        return

    if 0 <= index < len(faq_list):
        item = faq_list[index]
        text = f"❓ <b>{item['question']}</b>\n\n{item['answer']}"
        keyboard = [
            [InlineKeyboardButton("⬅️ Back to FAQ", callback_data="faq_back")]
        ]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(texts.RULES_MESSAGE, parse_mode="HTML")

handlers = [
    CommandHandler("start", start_command),
    CommandHandler(["help", "faq"], faq_command),
    CommandHandler("rules", rules_command),
    CallbackQueryHandler(faq_button_callback, pattern="^faq_"),
]