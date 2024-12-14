from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers import start, forward_message_to_admin, reply_to_user, broadcast, users, notify_admin_user_blocked

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_user))  # Allows admin to reply to users
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", users))
    app.add_handler(MessageHandler(filters.StatusUpdate.BOT_BLOCKED, notify_admin_user_blocked))

    app.run_polling()

if __name__ == "__main__":
    main()
