"""Default text templates and example configuration for FVCL_Bot.

To customize these settings without modifying the codebase, mount or place
your own custom `texts.py` inside the `DATA_DIR` directory (default: `./data/texts.py`
or `/data/texts.py` in Docker/Kubernetes).
"""

################################################################################
# General Configuration & Example Data
################################################################################
FAQ_DATA = [
    {
        "question": "🛋 What is the Crew Lounge?",
        "answer": "The Crew Lounge is a place to recover and rest. You can relax, grab food and drinks, and take a break from the convention!",
    },
    {
        "question": "📍 Where can I find the Crew Lounge?",
        "answer": "The Crew Lounge is located in <b>Room 0-3 on the ground floor</b>, right behind ConOps!",
    },
    {
        "question": "⏰ When is the Crew Lounge open?",
        "answer": "The Crew Lounge is open daily during the convention operating hours!",
    },
    {
        "question": "🧑‍✈️ Who can use the Crew Lounge?",
        "answer": "The Crew Lounge is open to all registered Crew members of the convention!",
    },
    {
        "question": "📜 What are the rules?",
        "answer": "The rules are simple. To view them, use /rules",
    },
]

REFILL_ITEMS = {
    "Water": "Still / Sparkling Water",
    "SoftDrinks": "Soft Drinks",
    "Coffee": "Coffee / Tea / Milk",
    "Fruit": "Fresh Fruit",
    "Snacks": "Sweet & Salty Snacks",
    "Cups": "Cups & Napkins",
}

OPENING_HOURS = {
    "Monday": {"open": "08:00", "close": "22:00"},
    "Tuesday": {"open": "08:00", "close": "22:00"},
    "Wednesday": {"open": "08:00", "close": "22:00"},
    "Thursday": {"open": "08:00", "close": "22:00"},
    "Friday": {"open": "08:00", "close": "22:00"},
    "Saturday": {"open": "08:00", "close": "22:00"},
    "Sunday": {"open": "08:00", "close": "22:00"},
}

################################################################################
# General Messages
################################################################################
START_MESSAGE = (
    "Hello, {name}! 👋\n"
    "I'm the Crew Lounge Bot and I'm here to help you with your needs!\n"
    "I will forward your request to the Crew Lounge On Duty and they will help you!\n\n"
    "You can use the following commands:\n"
    "- /start: Shows this message\n"
    "- /faq: Shows all information about the Crew Lounge\n"
    "- /refill: When something needs to be refilled\n"
    "- /report: When something is wrong, report it to the crew!\n"
    "- /rules: Shows the rules of the Crew Lounge"
)

FAQ_MESSAGE = (
    "Hi! 👋\n"
    "Do you have a question about the Crew Lounge? Check out the most common questions below!\n"
    "If your question is not in the list, please contact the Crew Lounge Team!\n\n"
)

RULES_MESSAGE = (
    "These are the rules of the Crew Lounge. Please read them carefully and follow them at all times.\n"
    "We are happy to provide a space for you to relax, so please help us keep it that way! Thank you!\n"
    "~Crew Lounge Team &lt;3\n\n"
    "1. Do not take food from the Crew Lounge outside of the Crew Lounge.\n"
    "2. Only Crew is allowed to enter the Crew Lounge.\n"
    "3. Do not refill items on your own. Please use the /refill command to let us know when something needs to be restocked.\n"
    "4. When you leave the Crew Lounge, please leave it clean and tidy.\n"
    "5. Food and drinks are free for crew members. Please be fair and considerate!\n"
    "6. Food and drinks in the lounge are intended as snacks in between and do not replace a full meal.\n"
)

################################################################################
# Refill Messages
################################################################################
REFILL_PROMPT = (
    "Something's empty? No worries!\n"
    "Just tell me what needs to be refilled:"
)

REFILL_CONFIRMATION = (
    "Thank you <b>{name}</b>!\n"
    "I've let the Crew Lounge On Duty know that <b>{item}</b> needs to be refilled."
)

CREW_REFILL_NOTIFICATION = (
    "🚨 <b>REFILL REQUEST</b>\n\n"
    "<b>What:</b> {item}\n"
    "<b>Reported by:</b> {user} (@{username})\n\n"
    "Please refill it as soon as possible!"
)

NO_REFILL_OPTIONS = "Currently, no refill options are available."
ITEM_NOT_AVAILABLE = "This item is no longer available."

################################################################################
# Report Messages
################################################################################
REPORT_PROMPT = (
    "Something's wrong in the Crew Lounge? Here you can report it!\n"
    "Please describe what's wrong and the Crew Lounge On Duty will help you!"
)

REPORT_CONFIRMATION = (
    "Thank you <b>{name}</b>, I've forwarded your report!\n"
    "A member of the Crew Lounge team will be there shortly! 🏃💨"
)

REPORT_CANCEL_CONFIRMATION = (
    "Alright, your report has been cancelled!"
)

CREW_REPORT_NOTIFICATION = (
    "🚨 <b>REPORT TO CL-TEAM</b>\n\n"
    "<b>Reported by:</b> {user} (@{username})\n"
    "<b>Report:</b> {report}\n\n"
    "Please help them as soon as possible!"
)

REPORT_EMPTY_ERROR = "Your report cannot be empty. Please briefly describe what happened:"
REPORT_TOO_LONG_ERROR = "Your report is too long (maximum {max_length} characters). Please be more concise:"
REPORT_NON_TEXT_ERROR = "⚠️ Please send your report exclusively as a text message or use the 'Cancel' button."

################################################################################
# Status & Action Alerts
################################################################################
CLOSED_NOTIFICATION = "<b>⚠️ The Crew Lounge team is currently off duty, but I've still forwarded your request. They will get back to you soon!</b>"
COOLDOWN_WARNING = "⚠️ Please wait another {remaining} second(s) before sending another request!"

BUTTON_MARK_DONE = "✅ Mark as done"
BUTTON_ON_MY_WAY = "🏃 On my way"
CREW_DONE = "<b>Done by: {user} (@{username}) at {time_done}</b>"
CREW_ON_MY_WAY = "🏃 <b>On the way: {user} (@{username}) at {time}</b>"

TASK_UNAUTHORIZED_ALERT = "⛔ Only the Crew Team can mark this task as done!"
TASK_UNAUTHORIZED_ON_MY_WAY_ALERT = "⛔ Only the Crew Team can accept this task!"
TASK_ALREADY_DONE_ALERT = "This task has already been marked as done."
TASK_ALREADY_ON_MY_WAY_ALERT = "Someone is already on the way or this task is already done."
TASK_ACTION_FAILED_ALERT = "Action could not be executed."
TASK_DONE_CONFIRMATION = "Marked as done! ✅"
TASK_ON_MY_WAY_CONFIRMATION = "You are on the way! 🏃"

NO_USERNAME = "No Username"
UNKNOWN_USER = "Unknown"
