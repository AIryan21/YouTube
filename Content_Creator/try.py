import asyncio
import threading
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update, Poll

# Define your bot token
TOKEN = '7096546771:AAHfk3avclrgDCyx4WkfKZJU3GFlPB_4dA4'  # Replace with your actual bot token

# Global variable to store the latest user update & context
latest_update = None
latest_context = None  

# Create the Telegram bot application
app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start command"""
    await update.message.reply_text("Welcome! Chat with me or create polls using /poll:Question|Option1|Option2|")

async def send_poll(poll_text: str):
    """Creates a poll or quiz from the input text"""
    global latest_update, latest_context
    if not latest_update or not latest_context:
        print("❌ No active chat to send a poll!")
        return

    try:
        parts = poll_text.replace("/poll:", "").split("|")
        question = parts[0].strip()
        options = []
        correct_option_id = None

        for i, opt in enumerate(parts[1:]):
            if opt.startswith("*"):  # Correct answer marked with '*'
                correct_option_id = i  
                options.append(opt[1:].strip())  
            else:
                options.append(opt.strip())

        if len(options) < 2:
            print("❌ Poll must have at least two options!")
            return

        if correct_option_id is not None:
            # Send a quiz if a correct answer is specified
            await latest_context.bot.send_poll(
                latest_update.effective_chat.id,
                question,
                options,
                type=Poll.QUIZ,
                correct_option_id=correct_option_id,
                is_anonymous=False
            )
        else:
            # Send a normal poll
            await latest_context.bot.send_poll(
                latest_update.effective_chat.id,
                question,
                options,
                is_anonymous=False
            )

        print(f"✅ Poll sent: {question}")

    except Exception as e:
        print(f"❌ Error creating poll: {str(e)}")

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stores the latest update so admin can reply"""
    global latest_update, latest_context
    latest_update = update
    latest_context = context
    print(f"User: {update.message.text}")

def admin_input():
    """Allows admin to send messages or polls anytime"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    while True:
        bot_response = input("Bot (type message or /poll:...): ").strip()

        if latest_update and latest_context:
            if bot_response.startswith("/poll:"):
                loop.run_until_complete(send_poll(bot_response))
            elif bot_response:  # Prevent sending empty messages
                loop.run_until_complete(latest_update.message.reply_text(bot_response))
            else:
                print("⚠️ Empty message ignored.")

# Start admin input thread
threading.Thread(target=admin_input, daemon=True).start()

# Handlers
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

# Start bot
if __name__ == '__main__':
    print("🚀 Bot is running...")
    app.run_polling()
