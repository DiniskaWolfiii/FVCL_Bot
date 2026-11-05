"""Helper functions and security utilities for FVCL_Bot.

Includes HTML sanitizing, user mention formatting, timezone/opening hours checks,
anti-spam cooldown tracking, and UI markup generators.
"""

import html
import time
import logging
from datetime import datetime
from typing import Optional, Tuple
from telegram import User, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.error import TelegramError

import config
import texts

logger = logging.getLogger(__name__)

# In-memory storage for anti-spam cooldowns: (user_id, action) -> timestamp
_user_cooldowns: dict[Tuple[int, str], float] = {}


def escape_html(text: Optional[str]) -> str:
    """Escapes special characters (&, <, >) safely for Telegram HTML parse_mode."""
    if text is None:
        return ""
    return html.escape(str(text), quote=False)


def format_user_mention(user: Optional[User]) -> str:
    """Returns an HTML-safe representation of the user.

    Example: 'John Doe (@johndoe)' or 'John Doe'.
    """
    if not user:
        return texts.UNKNOWN_USER

    safe_name = escape_html(user.full_name)
    if user.username:
        safe_username = escape_html(user.username)
        return f"{safe_name} (@{safe_username})"
    return safe_name


def get_current_time_str(time_format: str = "%H:%M") -> str:
    """Returns the current time in the configured timezone as a formatted string."""
    return datetime.now(config.TIMEZONE).strftime(time_format)


def is_lounge_open() -> bool:
    """Checks timezone-aware whether the Crew Lounge is currently open."""
    data = config.get_opening_data()
    now_dt = datetime.now(config.TIMEZONE)
    current_day = now_dt.strftime("%A")

    day_data = data.get(current_day)
    if not day_data or "open" not in day_data or "close" not in day_data:
        return False

    now_time = now_dt.time()
    try:
        open_time = datetime.strptime(day_data["open"], "%H:%M").time()
        close_time = datetime.strptime(day_data["close"], "%H:%M").time()
        return open_time <= now_time <= close_time
    except ValueError as e:
        logger.error("Invalid time format in opening.json for %s: %s", current_day, e)
        return False


def get_task_keyboard(show_on_my_way: bool = True) -> InlineKeyboardMarkup:
    """Creates the inline keyboard for crew tasks.

    If show_on_my_way is True, displays both 'On my way' and 'Mark as done' buttons.
    Otherwise, displays only the 'Mark as done' button.
    """
    if show_on_my_way:
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(texts.BUTTON_ON_MY_WAY, callback_data="on_my_way"),
                InlineKeyboardButton(texts.BUTTON_MARK_DONE, callback_data="done"),
            ]
        ])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(texts.BUTTON_MARK_DONE, callback_data="done")]
    ])


def get_done_keyboard() -> InlineKeyboardMarkup:
    """Creates the inline keyboard containing only the 'Mark as done' button."""
    return get_task_keyboard(show_on_my_way=False)


def check_user_cooldown(
    user_id: int, action: str, cooldown_seconds: int = config.ACTION_COOLDOWN_SECONDS
) -> Tuple[bool, int]:
    """Checks whether a user is still on cooldown for a given action.

    Returns (is_allowed, remaining_seconds).
    If is_allowed is True, the cooldown timer is automatically updated.
    """
    now = time.time()
    key = (user_id, action)
    last_time = _user_cooldowns.get(key, 0.0)
    elapsed = now - last_time

    if elapsed < cooldown_seconds:
        remaining = int(cooldown_seconds - elapsed) + 1
        return False, remaining

    _user_cooldowns[key] = now
    return True, 0


async def safe_remove_reply_markup(bot: Bot, chat_id: int, message_id: int) -> None:
    """Safely removes inline buttons from a message, catching TelegramErrors."""
    try:
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=None,
        )
    except TelegramError as e:
        # Message was deleted or is no longer editable
        logger.debug("Could not remove reply_markup for message %s: %s", message_id, e)
