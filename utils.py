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


def _build_task_callback(
    action: str,
    task_type: Optional[str] = None,
    user_id: Optional[int] = None,
    item_key: Optional[str] = None,
) -> str:
    """Builds a Telegram callback_data string (max 64 bytes) for crew task buttons."""
    if not task_type or user_id is None:
        return action
    base = f"{action}:{task_type}:{user_id}"
    if item_key:
        with_item = f"{base}:{item_key}"
        if len(with_item.encode("utf-8")) <= 64:
            return with_item
    return base


def parse_task_callback_data(
    data: Optional[str],
) -> Tuple[str, Optional[str], Optional[int], Optional[str]]:
    """Parses callback_data from crew task buttons into (action, task_type, user_id, item_key)."""
    if not data:
        return "", None, None, None
    parts = data.split(":", 3)
    action = parts[0]
    task_type = parts[1] if len(parts) > 1 and parts[1] else None
    user_id: Optional[int] = None
    if len(parts) > 2 and parts[2]:
        try:
            user_id = int(parts[2])
        except ValueError:
            user_id = None
    item_key = parts[3] if len(parts) > 3 and parts[3] else None
    return action, task_type, user_id, item_key


def get_task_keyboard(
    show_on_my_way: bool = True,
    task_type: Optional[str] = None,
    user_id: Optional[int] = None,
    item_key: Optional[str] = None,
) -> InlineKeyboardMarkup:
    """Creates the inline keyboard for crew tasks.

    If show_on_my_way is True, displays both 'On my way' and 'Mark as done' buttons.
    Otherwise, displays only the 'Mark as done' button.
    """
    on_my_way_cb = _build_task_callback("on_my_way", task_type, user_id, item_key)
    done_cb = _build_task_callback("done", task_type, user_id, item_key)

    if show_on_my_way:
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(texts.BUTTON_ON_MY_WAY, callback_data=on_my_way_cb),
                InlineKeyboardButton(texts.BUTTON_MARK_DONE, callback_data=done_cb),
            ]
        ])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(texts.BUTTON_MARK_DONE, callback_data=done_cb)]
    ])


def get_done_keyboard(
    task_type: Optional[str] = None,
    user_id: Optional[int] = None,
    item_key: Optional[str] = None,
) -> InlineKeyboardMarkup:
    """Creates the inline keyboard containing only the 'Mark as done' button."""
    return get_task_keyboard(
        show_on_my_way=False,
        task_type=task_type,
        user_id=user_id,
        item_key=item_key,
    )


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
