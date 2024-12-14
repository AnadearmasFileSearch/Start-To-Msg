from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers import start, forward_message_to_admin, reply_to_user
from handlers import broadcast, users

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    
    # Forward all text messages to admin (only for users)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))

    # Admin replies to the forwarded messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_user))

    # Admin-only commands
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", users))

    app.run_polling()

if __name__ == "__main__":
    main()
