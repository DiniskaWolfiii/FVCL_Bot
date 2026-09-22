from telegram.ext import Application, CommandHandler
from . import general, report

def register_handlers(app: Application):
    modules = [general, report]
    for module in modules:
        for handler in getattr(module, "handlers", []):
            app.add_handler(handler)
