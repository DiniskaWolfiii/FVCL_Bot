# Furvester Crew Lounge Bot

A simple Telegram bot to help manage the Crew Lounge at a convention with the following features:
- Alert Crew Lounge members to restock items when they're running low (`/refill`)
- Report issues if something is broken or needs attention (`/report`)
- View FAQs and rules of the Crew Lounge (`/faq`, `/rules`)
- Interactive task handling in the Crew Chat (`🏃 On my way` & `✅ Mark as done`)

---

## Prerequisites: Telegram Bot Setup

Before running the bot, set up your Telegram Bot:
1. Register a bot with [@BotFather](https://t.me/botfather). This gives you the `BOT_TOKEN`.
2. Add your bot to the Crew Chat.
3. Get the ID of your Crew Chat (`CREW_CHAT_ID`), e.g. by opening [Telegram Web](https://web.telegram.org/) and selecting the chat. For example, `https://web.telegram.org/k/#-1001234567890` corresponds to `-1001234567890`.

---

## Customizing Texts, Items & Opening Hours

The repository includes a default example [texts.py](texts.py).
On startup, the bot checks `DATA_DIR` (defaults to `/data` in Docker/Kubernetes or `./data` locally):
- If `DATA_DIR/texts.py` does not exist yet, the default `texts.py` is copied there automatically.
- If `DATA_DIR/texts.py` exists, it overrides the built-in `texts.py` so you can customize `FAQ_DATA`, `REFILL_ITEMS`, `OPENING_HOURS`, and all message templates without modifying the codebase.

---

## Option 1: Docker Compose

You can run the bot using [Docker Compose](https://www.docker.com/):

```yaml
services:
  fvcl_bot:
    container_name: fvcl_bot
    image: ghcr.io/diniskawolfiii/fvcl_bot:latest
    restart: unless-stopped
    volumes:
      - ./data:/data
    environment:
      - BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
      - CREW_CHAT_ID=<YOUR_CREW_CHAT_ID>
      - BOT_TIMEZONE=Europe/Berlin
      - ACTION_COOLDOWN_SECONDS=15
```

---

## Option 2: Kubernetes (k3s + ArgoCD GitOps)

Production deployment uses a separate private GitOps repository (`fvcl-bot-gitops`):
- **Public Code Repository (`FVCL_Bot`)**: Contains the application code, `Dockerfile`, and example configuration. Pushing to `main` builds a multi-arch container image (`linux/amd64`, `linux/arm64`), publishes `ghcr.io/diniskawolfiii/fvcl_bot:sha-<commit>`, and automatically updates `kustomization.yaml` in the private GitOps repository via `GITOPS_TOKEN`.
- **Private GitOps Repository (`fvcl-bot-gitops`)**: Holds the Kubernetes manifests (`k8s/`), `kustomization.yaml`, `argocd/application.yaml`, and the customized `texts.py` mounted via Kustomize `configMapGenerator`.

---

## Option 3: Local Development

1. Copy `.env.example` to `.env` and fill in your `BOT_TOKEN` and `CREW_CHAT_ID`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python main.py
   ```

---

## Contribution

Feel free to open a Pull Request or an Issue! Changes on feature branches are automatically tested via GitHub Actions and only deployed once merged into `main`.
