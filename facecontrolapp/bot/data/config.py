import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = [
    os.getenv("ADMIN_ID"),
]

# ip = os.getenv("ip")
IG_USER = str(os.getenv('IG_USER'))
IG_PASS = str(os.getenv('IG_PASS'))
