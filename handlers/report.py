"""Handlers for the incident reporting and task management workflow of FVCL_Bot.

Contains the multi-step report conversation (ConversationHandler) and the
crew team resolution workflow ('Mark as done').
"""

import logging
import warnings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.warnings import PTBUserWarning
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Silence PTBUserWarning for mixed message/callback ConversationHandlers
warnings.filterwarnings("ignore", category=PTBUserWarning, message=r".*per_message=False.*")

import config
import texts
import utils

logger = logging.getLogger(__name__)

WAITING_FOR_REPORT = 1
MAX_REPORT_LENGTH = 1000


async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the incident reporting process and prompts the user for details."""
    if not update.effective_message or not update.effective_user:
        return ConversationHandler.END

    user = update.effective_user

    # Anti-spam / cooldown check
    allowed, remaining = utils.check_user_cooldown(user.id, "report")
    if not allowed:
        await update.effective_message.reply_text(
            texts.COOLDOWN_WARNING.format(remaining=remaining)
        )
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton("Cancel", callback_data="report_cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = await update.effective_message.reply_text(
        text=texts.REPORT_PROMPT,
        reply_markup=reply_markup,
    )

    # Save prompt message ID to remove the Cancel button later
    context.user_data["report_prompt_msg_id"] = msg.message_id
    return WAITING_FOR_REPORT


async def receive_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processes user report text, validates it, and forwards it to the crew team."""
    if not update.effective_message or not update.effective_user:
        return ConversationHandler.END

    # Remove Cancel button from the previous bot prompt message
    prompt_msg_id = context.user_data.pop("report_prompt_msg_id", None)
    if prompt_msg_id and update.effective_chat:
        await utils.safe_remove_reply_markup(
            context.bot, update.effective_chat.id, prompt_msg_id
        )

    raw_text = update.effective_message.text or ""
    report_text = raw_text.strip()
    user = update.effective_user

    # Validation: prevent empty messages
    if not report_text:
        await update.effective_message.reply_text(texts.REPORT_EMPTY_ERROR)
        return WAITING_FOR_REPORT

    # Validation: enforce character limit against payload flooding
    if len(report_text) > MAX_REPORT_LENGTH:
        await update.effective_message.reply_text(
            texts.REPORT_TOO_LONG_ERROR.format(max_length=MAX_REPORT_LENGTH)
        )
        return WAITING_FOR_REPORT

    # HTML safety: escape all dynamic variables
    safe_name = utils.escape_html(user.first_name)
    safe_full_name = utils.escape_html(user.full_name)
    safe_username = utils.escape_html(user.username or texts.NO_USERNAME)
    safe_report = utils.escape_html(report_text)

    # 1. Confirmation sent back to the reporting user
    report_confirmation = texts.REPORT_CONFIRMATION.format(name=safe_name)
    if not utils.is_lounge_open():
        report_confirmation += f"\n\n{texts.CLOSED_NOTIFICATION}"

    await update.effective_message.reply_text(
        text=report_confirmation,
        parse_mode="HTML",
    )

    # 2. Notification forwarded to the crew lounge chat
    if config.CREW_CHAT_ID:
        crew_msg = texts.CREW_REPORT_NOTIFICATION.format(
            user=safe_full_name,
            username=safe_username,
            report=safe_report,
        )
        try:
            await context.bot.send_message(
                chat_id=config.CREW_CHAT_ID,
                text=crew_msg,
                parse_mode="HTML",
                reply_markup=utils.get_task_keyboard(),
            )
        except Exception as e:
            logger.error(
                "Failed to send report notification to CREW_CHAT_ID %s: %s",
                config.CREW_CHAT_ID,
                e,
            )

    return ConversationHandler.END


async def non_text_report_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles unsupported media inputs (stickers, photos, voice notes) during reporting."""
    if update.effective_message:
        await update.effective_message.reply_text(texts.REPORT_NON_TEXT_ERROR)
    return WAITING_FOR_REPORT


async def cancel_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the report process via /cancel command."""
    prompt_msg_id = context.user_data.pop("report_prompt_msg_id", None)
    if prompt_msg_id and update.effective_chat:
        await utils.safe_remove_reply_markup(
            context.bot, update.effective_chat.id, prompt_msg_id
        )

    if update.effective_message:
        await update.effective_message.reply_text(
            text=texts.REPORT_CANCEL_CONFIRMATION
        )
    return ConversationHandler.END


async def cancel_report_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the report process via the 'Cancel' inline button click."""
    query = update.callback_query
    if not query:
        return ConversationHandler.END

    await query.answer()
    context.user_data.pop("report_prompt_msg_id", None)

    await query.edit_message_text(text=texts.REPORT_CANCEL_CONFIRMATION)
    return ConversationHandler.END


async def on_my_way_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Marks a task as 'On my way' in the crew chat, records who is on the way, and updates buttons."""
    query = update.callback_query
    if not query or not query.message:
        return

    # Authorization check: only allow clicks originating from the crew chat
    if config.CREW_CHAT_ID and query.message.chat_id != config.CREW_CHAT_ID:
        await query.answer(
            texts.TASK_UNAUTHORIZED_ON_MY_WAY_ALERT,
            show_alert=True,
        )
        return

    original_html = query.message.text_html or ""

    # Check if task was already completed
    if "<s>" in original_html:
        await query.answer(texts.TASK_ALREADY_DONE_ALERT, show_alert=True)
        return

    # Check if someone is already on the way
    if "🏃 <b>On the way:" in original_html:
        await query.answer(texts.TASK_ALREADY_ON_MY_WAY_ALERT, show_alert=True)
        return

    user = query.from_user
    time_str = utils.get_current_time_str("%H:%M")

    safe_full_name = utils.escape_html(user.full_name)
    safe_username = utils.escape_html(user.username or texts.NO_USERNAME)

    on_way_text = texts.CREW_ON_MY_WAY.format(
        user=safe_full_name,
        username=safe_username,
        time=time_str,
    )

    updated_text = f"{original_html}\n\n{on_way_text}"

    try:
        await query.edit_message_text(
            text=updated_text,
            parse_mode="HTML",
            reply_markup=utils.get_done_keyboard(),
        )
        await query.answer(texts.TASK_ON_MY_WAY_CONFIRMATION)
    except BadRequest as e:
        # Handle race conditions / double clicks gracefully
        if "Message is not modified" in str(e):
            await query.answer(texts.TASK_ALREADY_ON_MY_WAY_ALERT, show_alert=True)
        else:
            logger.warning("Error marking task as on the way: %s", e)
            await query.answer(texts.TASK_ACTION_FAILED_ALERT, show_alert=True)


async def mark_done_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Marks a task as completed in the crew chat, strikes through text, and removes the button."""
    query = update.callback_query
    if not query or not query.message:
        return

    # Authorization check: only allow clicks originating from the crew chat
    if config.CREW_CHAT_ID and query.message.chat_id != config.CREW_CHAT_ID:
        await query.answer(
            texts.TASK_UNAUTHORIZED_ALERT,
            show_alert=True,
        )
        return

    original_html = query.message.text_html or ""

    # Prevent double clicks if already completed
    if "<s>" in original_html:
        await query.answer(texts.TASK_ALREADY_DONE_ALERT, show_alert=True)
        return

    user = query.from_user
    time_done = utils.get_current_time_str("%H:%M")

    safe_full_name = utils.escape_html(user.full_name)
    safe_username = utils.escape_html(user.username or texts.NO_USERNAME)

    done_text = texts.CREW_DONE.format(
        user=safe_full_name,
        username=safe_username,
        time_done=time_done,
    )

    # Strike through original message and append completion details
    updated_text = f"<s>{original_html}</s>\n\n{done_text}"

    try:
        await query.edit_message_text(
            text=updated_text,
            parse_mode="HTML",
        )
        await query.answer(texts.TASK_DONE_CONFIRMATION)
    except BadRequest as e:
        # Handle race conditions / double clicks gracefully
        if "Message is not modified" in str(e):
            await query.answer(texts.TASK_ALREADY_DONE_ALERT, show_alert=True)
        else:
            logger.warning("Error marking task as done: %s", e)
            await query.answer(texts.TASK_ACTION_FAILED_ALERT, show_alert=True)


report_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("report", report_command)],
    states={
        WAITING_FOR_REPORT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_report),
            MessageHandler(~filters.TEXT & ~filters.COMMAND, non_text_report_handler),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel_report),
        CallbackQueryHandler(cancel_report_callback, pattern="^report_cancel$"),
    ],
    per_message=False,
)

handlers = [
    CallbackQueryHandler(on_my_way_callback, pattern="^on_my_way$"),
    CallbackQueryHandler(mark_done_callback, pattern="^done$"),
    report_conv_handler,
]
