import os
import logging
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, filters, Application
from config import BOT_TOKEN, ADMIN_ID, WEBHOOK_URL
from handlers import start, forward_message_to_admin, reply_to_user, broadcast, users  # Import your handlers

# Set up logging to get detailed information
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

# Initialize the Application object (v20.x and above)
application = Application.builder().token(BOT_TOKEN).build()

# Register command and message handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))
application.add_handler(CommandHandler("broadcast", broadcast))
application.add_handler(CommandHandler("users", users))
application.add_handler(MessageHandler(filters.TEXT & filters.Private, reply_to_user))

# This function sets the webhook for Telegram updates
def set_webhook():
    webhook_url = f'{WEBHOOK_URL}/{BOT_TOKEN}'
    bot.set_webhook(url=webhook_url)
    logger.info(f"Webhook set to {webhook_url}")

# This function will process incoming webhook requests
def process_update(request):
    update = Update.de_json(request.get_json(force=True), bot)
    application.process_update(update)

# The function to handle the webhook callback (without Flask)
def webhook(request):
    try:
        process_update(request)
        return "OK"
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return "Failed"

if __name__ == '__main__':
    # Register webhook
    set_webhook()

    # Start webhook handling (using werkzeug or any suitable server)
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5000, webhook)
