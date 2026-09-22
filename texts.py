################################################################################
# General
################################################################################
START_MESSAGE = (
    "Hello, {name}! 👋\n"
    "I'm the Furvester Crew Lounge Bot and I'm here to help you with your needs!\n"
    "Or more, I will forward your request to the Crew Lounge On Duty and they will help you!\n\n"
    "You can use following commands:\n"
    "- /start: Shows this message\n"
    "- /help: Shows a help message with all commands\n"
    "- /refill: When something needs to be refilled"
)

HELP_MESSAGE = (
    "Here's the help..."
)
################################################################################
# Report to CL-Team
################################################################################
REFILL_PROMPT = (
    "Somethings empty? No worries!\n"
    "Just tell me, what need's to be refilled?"
)
REFILL_CONFIRMATION = (
    "Thank you <b>{name}</b>!\n"
    "I've let the Crew Lounge On Duty know, that <b>{item}</b> needs to be refilled."
)
CREW_REFILL_NOTIFICATION = (
    "🚨 <b>REFILL REQUEST</b>\n\n"
    "<b>What:</b> {item}\n"
    "<b>Reported by:</b> {user} (@{username})\n\n"
    "Please refill it as soon as possible!"
)

REPORT_PROMPT = (
    "Somethings wrong in the Crew Lounge? Here you can report it!\n"
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