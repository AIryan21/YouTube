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

# Autonomous Bot Response Logic
def generate_bot_response(user_input: str) -> str:
    """
    This function should be replaced with your autonomous bot's logic.
    It will generate a response based on user input.
    """
    if "hello" in user_input.lower():
        return "Hello! How can I assist you today?"
    elif "help" in user_input.lower():
        return "I can send you polls, media files, and much more. Just ask!"
    elif "poll" in user_input.lower():
        return "/poll:What is your favorite color?|Red|Blue|Green"
    elif "send image" in user_input.lower():
        return "/image:path/to/image.jpg"
    elif "send audio" in user_input.lower():
        return "/audio:path/to/audio.mp3"
    elif "send video" in user_input.lower():
        return "/video:path/to/video.mp4"
    elif "send document" in user_input.lower():
        return "/document:path/to/file.pdf"
    else:
        return "I didn't understand that. Could you please clarify?"

# Handle /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start command"""
    await update.message.reply_text("Welcome! Use /poll:Question|Option1|Option2| or /options:Choose one|Yes|No")

# Function to send a file (image, audio, video, document)
async def send_file(file_type: str, file_path: str):
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

# Function to send a poll
async def send_poll(poll_text: str):
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

# Function to send inline options
async def send_options(options_text: str):
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

# Handle user input (messages) and route to autonomous response logic
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global latest_update, latest_context
    latest_update = update
    latest_context = context
    user_input = update.message.text
    print(f"User: {user_input}")

    # Autonomous bot response generation
    bot_response = generate_bot_response(user_input)
    
    # Process bot response
    if bot_response.startswith("/poll:"):
        await send_poll(bot_response)
    elif bot_response.startswith("/options:"):
        await send_options(bot_response)
    elif bot_response.startswith("/image:"):
        file_path = bot_response.replace("/image:", "").strip()
        await send_file("image", file_path)
    elif bot_response.startswith("/audio:"):
        file_path = bot_response.replace("/audio:", "").strip()
        await send_file("audio", file_path)
    elif bot_response.startswith("/video:"):
        file_path = bot_response.replace("/video:", "").strip()
        await send_file("video", file_path)
    elif bot_response.startswith("/document:"):
        file_path = bot_response.replace("/document:", "").strip()
        await send_file("document", file_path)
    else:
        await update.message.reply_text(bot_response)
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles button presses."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

# Admin input for testing purposes (can be replaced with autonomous bot logic)
def admin_input():
    """Allows admin to send messages, files, or interactive elements anytime"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    while True:
        bot_response = input("Bot (message, /poll:/options:/image:/audio:/video:/document:...): ").strip()

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

# Start admin input thread (for testing purposes)
threading.Thread(target=admin_input, daemon=True).start()

# Handlers
app.add_handler(CommandHandler('start', start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

# Start bot
if __name__ == '__main__':
    print("🚀 Bot is running...")
    app.run_polling()
