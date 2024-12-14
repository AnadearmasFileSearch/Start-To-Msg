import os
from dotenv import load_dotenv

# Load environment variables from .env (if running locally)
load_dotenv()

# Retrieve sensitive variables from environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URL = os.environ.get("MONGO_URL")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))  # Ensure it's an integer

# Ensure all necessary variables are set
if not BOT_TOKEN or not MONGO_URL or not ADMIN_ID:
    raise ValueError("Missing required environment variables. Please set BOT_TOKEN, MONGO_URL, and ADMIN_ID.")
