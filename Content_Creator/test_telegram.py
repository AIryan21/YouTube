from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from telegram import Update, InputFile

import os

# Define the token directly in the code
TOKEN = '7096546771:AAHfk3avclrgDCyx4WkfKZJU3GFlPB_4dA4'  # Replace with your actual bot token

def ask_multimodal_llm(input_data, input_type="text", model="gpt-4o-multimodal", timeout=30):
    """
    Communicate with the multimodal LLM to get a response.
    
    Parameters:
        input_data: str or bytes - The input to the LLM (text or file content).
        input_type: str - Type of input ('text', 'image', 'video').
        model: str - The LLM model to use.
        timeout: int - Timeout for the request.

    Returns:
        dict - Response from the LLM containing text or media.
    """
    # Simulate the response from the multimodal LLM (replace with actual API call)
    if input_type == "text":
        return {"type": "text", "data": f"Response to text: {input_data}"}
    elif input_type in ["image", "video"]:
        return {"type": "text", "data": f"Processed your {input_type} input."}
    else:
        return {"type": "text", "data": "Unsupported input type."}

# Create the Application instance with the token
app = ApplicationBuilder().token(TOKEN).build()

# Start command handler to initiate interaction with the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"User {update.effective_user.username} started the bot with /start command.")
    await update.message.reply_text("Welcome! I am a multimodal bot. Send me text, photos, videos, or drag and drop files into the terminal, and I'll respond!")

start_handler = CommandHandler('start', start)
app.add_handler(start_handler)

# Function to handle text messages
async def respond_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.effective_user.username or "Unknown"
    print(f"Text message from {user_name}: {user_message}")

    # Send text to LLM and get the response
    response = ask_multimodal_llm(user_message, input_type="text")
    await update.message.reply_text(response["data"])

# Function to handle photo messages
async def respond_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.username or "Unknown"
    photo = update.message.photo[-1]  # Get the highest resolution photo
    photo_file = await photo.get_file()
    print(f"Photo received from {user_name}. File ID: {photo.file_id}")

    # Download the photo
    photo_data = await photo_file.download_as_bytearray()
    response = ask_multimodal_llm(photo_data, input_type="image")

    await update.message.reply_text(response["data"])

# Function to handle video messages
async def respond_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.username or "Unknown"
    video = update.message.video
    print(f"Video received from {user_name}. File ID: {video.file_id}, File size: {video.file_size}")

    # Check for size limit
    if video.file_size > 40 * 1024 * 1024:
        await update.message.reply_text("Sorry, the video file is too large for processing (max 40 MB).")
        return

    video_file = await video.get_file()
    video_data = await video_file.download_as_bytearray()
    response = ask_multimodal_llm(video_data, input_type="video")

    await update.message.reply_text(response["data"])

# Function to handle file drag and drop
async def handle_file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = input("Drag and drop your file here: ").strip()  # User drags and drops the file
    if not os.path.exists(file_path):
        print("File does not exist. Please try again.")
        return

    try:
        with open(file_path, 'rb') as file:
            file_type = file_path.split('.')[-1].lower()
            if file_type in ['jpg', 'jpeg', 'png']:
                response = ask_multimodal_llm(file.read(), input_type="image")
            elif file_type in ['mp4', 'mkv', 'avi']:
                response = ask_multimodal_llm(file.read(), input_type="video")
            else:
                response = ask_multimodal_llm(file.read(), input_type="text")

            await context.bot.send_message(chat_id=update.effective_chat.id, text=response["data"])
    except Exception as e:
        print(f"Error processing the file: {e}")

# Message handlers for text, photo, video inputs, and file drag/drop
respond_text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, respond_text)
respond_photo_handler = MessageHandler(filters.PHOTO, respond_photo)
respond_video_handler = MessageHandler(filters.VIDEO, respond_video)
app.add_handler(respond_text_handler)
app.add_handler(respond_photo_handler)
app.add_handler(respond_video_handler)

# Handle unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Unknown command received from {update.effective_user.username}: {update.message.text}")
    await update.message.reply_text("Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(filters.COMMAND, unknown)
app.add_handler(unknown_handler)

# Start the bot
if __name__ == '__main__':
    print("The bot is starting...")
    app.run_polling()
    print("The bot has stopped.")
