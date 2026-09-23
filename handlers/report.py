from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
import texts
import config

WAITING_FOR_REPORT = 1

async def refill_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Zeigt die Auswahlbuttons an."""
    refill_options = config.get_refill_options()
    keyboard = []
    for key, label in refill_options.items():
        keyboard.append([InlineKeyboardButton(label, callback_data=key)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text(
        text=texts.REFILL_PROMPT,
        reply_markup=reply_markup
    )
async def refill_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reagiert auf den Klick eines Buttons."""
    query = update.callback_query
    await query.answer()  # Wichtig: Bestätigt Telegram den Klick (entfernt Lade-Icon)
    refill_options = config.get_refill_options()
    selected_key = query.data
    selected_label = refill_options.get(selected_key, "Unbekannt")
    user = query.from_user
    # 1. Nachricht beim Nutzer anpassen (Buttons verschwinden, Erfolgsmeldung)
    await query.edit_message_text(
        text=texts.REFILL_CONFIRMATION.format(
            name=user.first_name,
            item=selected_label
        ),
        parse_mode="HTML"
    )
    # 2. An die Crew Lounge Gruppe senden (falls CREW_CHAT_ID gesetzt ist)
    if config.CREW_CHAT_ID:
        crew_msg = texts.CREW_REFILL_NOTIFICATION.format(
            item=selected_label,
            user=user.full_name,
            username=user.username or "Kein Username"
        )
        await context.bot.send_message(
            chat_id=config.CREW_CHAT_ID,
            text=crew_msg,
            parse_mode="HTML"
        )

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Cancel", callback_data="report_cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text(
        text=texts.REPORT_PROMPT,
        reply_markup=reply_markup
    )
    return WAITING_FOR_REPORT

async def receive_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    report_text = update.message.text
    user = update.effective_user

    await update.effective_message.reply_text(
        text=texts.REPORT_CONFIRMATION.format(
            name=user.first_name
        ),
        parse_mode="HTML"
    )
    if config.CREW_CHAT_ID:
        crew_msg = texts.CREW_REPORT_NOTIFICATION.format(
            user=user.full_name,
            username=user.username or "Kein Username",
            report=report_text
        )
        await context.bot.send_message(
            chat_id=config.CREW_CHAT_ID,
            text=crew_msg,
            parse_mode="HTML"
        )
    return ConversationHandler.END

async def cancel_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        text=texts.REPORT_CANCEL_CONFIRMATION
    )
    return ConversationHandler.END

async def cancel_report_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Ersetzt den Prompt & entfernt den Button
    await query.edit_message_text(
        text=texts.REPORT_CANCEL_CONFIRMATION
    )
    return ConversationHandler.END

    
report_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("report", report_command)],
    states={
        WAITING_FOR_REPORT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_report)
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel_report),
        CallbackQueryHandler(cancel_report_callback, pattern="report_cancel")
    ]
)
handlers = [
    CommandHandler("refill", refill_command),
    CallbackQueryHandler(refill_button_callback, pattern="^refill_"),
    report_conv_handler,
]
