"""Handler registration for FVCL_Bot.

Aggregates general, refill, and report modules and registers their handlers
with the central Telegram Application.
"""

from telegram.ext import Application
from . import general, refill, report


def register_handlers(app: Application) -> None:
    """Registers all handlers from submodules into the provided Application."""
    modules = [general, refill, report]
    for module in modules:
        for handler in getattr(module, "handlers", []):
            app.add_handler(handler)
