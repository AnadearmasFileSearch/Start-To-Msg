import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")
ADMIN_ID = os.getenv("ADMIN_ID")  # Make sure this is an integer
PORT = os.getenv("PORT", 8080)  # Default to 8080 if not specified

# Optional: Validate the required variables
if not BOT_TOKEN or not MONGO_URL or not ADMIN_ID:
    raise ValueError("Missing required environment variables: BOT_TOKEN, MONGO_URL, or ADMIN_ID.")
