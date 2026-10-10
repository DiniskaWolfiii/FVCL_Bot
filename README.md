# Furvester Crew Lounge Bot

A simple bot to help manage the Crew Lounge at the yearly Furvester Furry Convention with following features:
- Alert Crew Lounge members to restock items when they're running low
- Report issues if something is broken or not working
- Watch FAQs and rules of the Crew Lounge

# Installation

The currently recommended way to install and run the bot is using [Docker](https://www.docker.com/). There is a pre-built image available that can be run with following `docker-compose.yml` file.

```yaml
services:
  fvcl-bot:
    image: ghcr.io/diniskawolfiii/fvcl-bot:latest
    restart: unless-stopped
    volumes:
      - 'bot-data:/data'
    environment:
      - BOT_TOKEN=<YOUR TELEGRAM BOT TOKEN>
      - CREW_CHAT_ID=<YOUR CREW CHAT ID>
volumes:
  bot-data:
```

Before you begin to run the bot, you will need to to setup your Telegram Bot:
1. Register a bot with [@BotFather](https://t.me/botfather). This will give you the token for your bot.
2. Add your bot to the Crew Chat.
3. Get the ID of your chat by opening [Telegram Web](https://web.telegram.org/) and selecting the chat with your bot. In the URL you will see the ID of the chat.  
For example: https://web.telegram.org/k/-1234567890123 would give you the ID -1234567890123.
4. Setup all the environment variables in the `docker-compose.yml` file.  
Don't forget to change the environment variables.
5. Run the bot using `docker-compose up -d`.

# Contribution

You want to contribute? 
Well... It is just an update bot for the Crew Lounge, it's not that deep lol.  
But hey! Feel free to make a PR or open an Issue. I will respond as soon as possible. (Maybe)
