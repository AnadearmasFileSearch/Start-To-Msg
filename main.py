from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ChatMemberHandler
from config import BOT_TOKEN
from handlers import start, forward_message_to_admin, reply_to_user
from handlers import broadcast, users, handle_user_blocked_or_deleted
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_user))  # Allows admin to reply to users
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", users))

    # Handle user blocking or deleting the bot
    app.add_handler(ChatMemberHandler(handle_user_blocked_or_deleted, ChatMemberHandler.MY_CHAT_MEMBER))

    # Add an error handler
    app.add_error_handler(error_handler)

    app.run_polling()

async def error_handler(update, context):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

if __name__ == "__main__":
    main()
