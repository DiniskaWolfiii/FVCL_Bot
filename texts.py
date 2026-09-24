################################################################################
# General
################################################################################
START_MESSAGE = (
    "Hello, {name}! 👋\n"
    "I'm the Furvester Crew Lounge Bot and I'm here to help you with your needs!\n"
    "Or more, I will forward your request to the Crew Lounge On Duty and they will help you!\n\n"
    "You can use following commands:\n"
    "- /start: Shows this message\n"
    "- /faq: Shows all information about the Crew Lounge\n"
    "- /refill: When something needs to be refilled\n"
    "- /report: When something is wrong, report stuff to the crew!\n"
    "- /rules: Shows the rules of the Crew Lounge"
)

FAQ_MESSAGE = (
    "Hi! 👋\n"
    "You have a question about the Crew Lounge? No Problem! Check out the most common questions below!\n"
    "Your question is not in the list? Contact the CL-Team!\n\n"
)

RULES_MESSAGE = (
    "These are the rules of the Crew Lounge. Please read them very carefully and follow them at any time.\n"
    "We are really happy to provide a space for you to relaxe, so help us to keep it that way! Thank you!\n"
    "~Crew Lounge Team &lt;3\n\n"
    "1. Do not take food from the Crew Lounge outside of the Crew Lounge.\n"
    "2. Only Crew is allowed to enter Crew Lounge. Not even a +1.\n"
    "3. Do not refill on your own. Please use the /refill command to let us know when something needs to be refilled. This helps us to keep track if we also need to refill our storage!\n"
    "4. When you leave the Crew Lounge, please leave it as you found it. Clean and tidy.\n"
    "5. Food and drinks are for free. But please be fair and dont take too much!\n"
    "6. Also, food and drinks are intended as a snack in between. They do not replace a full meal!\n"
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