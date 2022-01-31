import os
from os import getenv

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "NACBots")
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
ARQ_API_KEY = getenv("ARQ_API_KEY")
ARQ_API_URL = "https://grambuilders.tech/"
