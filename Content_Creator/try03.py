import asyncio
import threading
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Define your bot token
TOKEN = '7096546771:AAHfk3avclrgDCyx4WkfKZJU3GFlPB_4dA4'  # Replace with your actual bot token

# Global variables to store updates and context
latest_update = None
latest_context = None  

# Create the Telegram bot application
app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start command"""
    await update.message.reply_text("Welcome! Use /poll:Question|Option1|Option2| or /options:Choose one|Yes|No")

async def send_file(file_type: str, file_path: str):
    """Handles sending files (image, audio, video, document)"""
    global latest_update, latest_context
    if not latest_update or not latest_context:
        print("❌ No active chat to send a file!")
        return
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        if file_type == "image":
            await latest_context.bot.send_photo(latest_update.effective_chat.id, photo=open(file_path, 'rb'))
        elif file_type == "audio":
            await latest_context.bot.send_audio(latest_update.effective_chat.id, audio=open(file_path, 'rb'))
        elif file_type == "video":
            await latest_context.bot.send_video(latest_update.effective_chat.id, video=open(file_path, 'rb'))
        elif file_type == "document":
            await latest_context.bot.send_document(latest_update.effective_chat.id, document=open(file_path, 'rb'))

        print(f"✅ {file_type.capitalize()} sent: {file_path}")

    except Exception as e:
        print(f"❌ Error sending {file_type}: {str(e)}")

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
            if opt.startswith("*"):  # Mark correct answer with '*'
                correct_option_id = i  
                options.append(opt[1:].strip())  
            else:
                options.append(opt.strip())

        if len(options) < 2:
            print("❌ Poll must have at least two options!")
            return

        if correct_option_id is not None:
            await latest_context.bot.send_poll(
                latest_update.effective_chat.id,
                question,
                options,
                type=Poll.QUIZ,
                correct_option_id=correct_option_id,
                is_anonymous=False
            )
        else:
            await latest_context.bot.send_poll(
                latest_update.effective_chat.id,
                question,
                options,
                is_anonymous=False
            )

        print(f"✅ Poll sent: {question}")

    except Exception as e:
        print(f"❌ Error creating poll: {str(e)}")

async def send_options(options_text: str):
    """Creates an inline keyboard with selectable options"""
    global latest_update, latest_context
    if not latest_update or not latest_context:
        print("❌ No active chat to send options!")
        return

    try:
        parts = options_text.replace("/options:", "").split("|")
        question = parts[0].strip()
        options = [opt.strip() for opt in parts[1:]]

        if len(options) < 2:
            print("❌ At least two options are required!")
            return

        keyboard = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in options]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await latest_context.bot.send_message(
            chat_id=latest_update.effective_chat.id,
            text=question,
            reply_markup=reply_markup
        )
        print(f"✅ Options sent: {question}")

    except Exception as e:
        print(f"❌ Error creating options: {str(e)}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles button clicks and updates the message"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"✅ Selected: {query.data}")

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stores the latest update so admin can reply"""
    global latest_update, latest_context
    latest_update = update
    latest_context = context
    print(f"User: {update.message.text}")

def admin_input():
    """Allows admin to send messages, files, or interactive elements anytime"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    while True:
        bot_response = input("Bot : ").strip()

        if latest_update and latest_context:
            if bot_response.startswith("/poll:"):
                loop.run_until_complete(send_poll(bot_response))
            elif bot_response.startswith("/options:"):
                loop.run_until_complete(send_options(bot_response))
            elif bot_response.startswith("/image:"):
                file_path = bot_response.replace("/image:", "").strip()
                loop.run_until_complete(send_file("image", file_path))
            elif bot_response.startswith("/audio:"):
                file_path = bot_response.replace("/audio:", "").strip()
                loop.run_until_complete(send_file("audio", file_path))
            elif bot_response.startswith("/video:"):
                file_path = bot_response.replace("/video:", "").strip()
                loop.run_until_complete(send_file("video", file_path))
            elif bot_response.startswith("/document:"):
                file_path = bot_response.replace("/document:", "").strip()
                loop.run_until_complete(send_file("document", file_path))
            elif bot_response:
                loop.run_until_complete(latest_update.message.reply_text(bot_response))
            else:
                print("⚠️ Empty message ignored.")

# Start admin input thread
threading.Thread(target=admin_input, daemon=True).start()

# Handlers
app.add_handler(CommandHandler('start', start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

# Start bot
if __name__ == '__main__':
    print("🚀 Bot is running...")
    app.run_polling()
