"""General command handlers for FVCL_Bot.

Contains /start, /faq (with interactive inline navigation), and /rules.
"""

import logging
from typing import List, Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

import config
import texts
import utils

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets the user and lists available bot commands."""
    if not update.effective_message or not update.effective_user:
        return

    safe_name = utils.escape_html(update.effective_user.first_name)
    await update.effective_message.reply_text(
        text=texts.START_MESSAGE.format(name=safe_name),
        parse_mode="HTML",
    )


def build_faq_keyboard(faq_list: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    """Generates an inline keyboard listing all available FAQ questions."""
    keyboard = [
        [InlineKeyboardButton(item["question"], callback_data=f"faq_{i}")]
        for i, item in enumerate(faq_list)
    ]
    return InlineKeyboardMarkup(keyboard)


async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the interactive FAQ menu."""
    if not update.effective_message:
        return

    faq_list = config.get_faq_data()
    reply_markup = build_faq_keyboard(faq_list)

    await update.effective_message.reply_text(
        text=texts.FAQ_MESSAGE,
        reply_markup=reply_markup,
        parse_mode="HTML",
    )


async def faq_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles clicks on FAQ questions or the back button."""
    query = update.callback_query
    if not query:
        return

    await query.answer()
    faq_list = config.get_faq_data()

    if query.data == "faq_back":
        await query.edit_message_text(
            text=texts.FAQ_MESSAGE,
            reply_markup=build_faq_keyboard(faq_list),
            parse_mode="HTML",
        )
        return

    if not query.data or not query.data.startswith("faq_"):
        return

    try:
        index = int(query.data.split("_", 1)[1])
    except (IndexError, ValueError):
        return

    if 0 <= index < len(faq_list):
        item = faq_list[index]
        safe_q = utils.escape_html(item.get("question", ""))
        safe_a = utils.escape_html(item.get("answer", ""))
        text = f"❓ <b>{safe_q}</b>\n\n{safe_a}"

        keyboard = [
            [InlineKeyboardButton("⬅️ Back to FAQ", callback_data="faq_back")]
        ]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the Crew Lounge rules."""
    if not update.effective_message:
        return

    await update.effective_message.reply_text(
        text=texts.RULES_MESSAGE,
        parse_mode="HTML",
    )


handlers = [
    CommandHandler("start", start_command),
    CommandHandler(["help", "faq"], faq_command),
    CommandHandler("rules", rules_command),
    CallbackQueryHandler(faq_button_callback, pattern="^faq_"),
]