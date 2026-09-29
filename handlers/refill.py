"""Handlers for the refill workflow of FVCL_Bot.

Allows crew members to request supply refills with anti-spam protection,
status checking, and forwarding to the crew chat.
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

import config
import texts
import utils

logger = logging.getLogger(__name__)


async def refill_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays selection buttons for refill items."""
    if not update.effective_message:
        return

    refill_options = config.get_refill_options()
    if not refill_options:
        await update.effective_message.reply_text(texts.NO_REFILL_OPTIONS)
        return

    keyboard = [
        [InlineKeyboardButton(label, callback_data=key)]
        for key, label in refill_options.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.effective_message.reply_text(
        text=texts.REFILL_PROMPT,
        reply_markup=reply_markup,
    )


async def refill_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles clicks on refill selection buttons."""
    query = update.callback_query
    if not query:
        return

    user = query.from_user
    selected_key = query.data or ""

    # Anti-spam / cooldown check
    allowed, remaining = utils.check_user_cooldown(user.id, "refill")
    if not allowed:
        await query.answer(
            texts.COOLDOWN_WARNING.format(remaining=remaining),
            show_alert=True,
        )
        return

    await query.answer()

    refill_options = config.get_refill_options()
    if selected_key not in refill_options:
        await query.answer(texts.ITEM_NOT_AVAILABLE, show_alert=True)
        return

    selected_label = refill_options[selected_key]
    safe_item = utils.escape_html(selected_label)
    safe_name = utils.escape_html(user.first_name)
    safe_full_name = utils.escape_html(user.full_name)
    safe_username = utils.escape_html(user.username or texts.NO_USERNAME)

    # 1. Confirmation sent back to the requesting user
    refill_confirmation = texts.REFILL_CONFIRMATION.format(
        name=safe_name,
        item=safe_item,
    )
    if not utils.is_lounge_open():
        refill_confirmation += f"\n\n{texts.CLOSED_NOTIFICATION}"

    await query.edit_message_text(
        text=refill_confirmation,
        parse_mode="HTML",
    )

    # 2. Notification forwarded to the crew lounge chat
    if config.CREW_CHAT_ID:
        crew_msg = texts.CREW_REFILL_NOTIFICATION.format(
            item=safe_item,
            user=safe_full_name,
            username=safe_username,
        )
        await context.bot.send_message(
            chat_id=config.CREW_CHAT_ID,
            text=crew_msg,
            parse_mode="HTML",
            reply_markup=utils.get_task_keyboard(),
        )


handlers = [
    CommandHandler("refill", refill_command),
    CallbackQueryHandler(refill_button_callback, pattern="^refill_"),
]
