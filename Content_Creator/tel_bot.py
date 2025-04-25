from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from telegram import Update

# Define the token directly in the code
TOKEN = '7096546771:AAHfk3avclrgDCyx4WkfKZJU3GFlPB_4dA4'  # Replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token

def ask_duckduckgo_chat(user_input):
    print(user_input)
    reply =input("Enter:")
    return reply
    
# Create the Application instance with the token
app = ApplicationBuilder().token(TOKEN).build()

# Start command handler to initiate interaction with the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Log user command to terminal
    print(f"User {update.effective_user.username} started the bot with /start command.")
    
    await update.message.reply_text("Welcome! I'm a bot. You can talk to me!")

start_handler = CommandHandler('start', start)
app.add_handler(start_handler)

# Function to handle text messages and respond with simple logic
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()  # Convert user input to lowercase for easier comparison
    user_name = update.effective_user.username or "Unknown"
    
    # Log the user input to the terminal
    print(f"Message from {user_name}: {user_message}")
    
    user_input=user_message
    bot_response = ask_duckduckgo_chat(user_input)
    await update.message.reply_text(bot_response)
    print(f"Message from bot: {bot_response}")
    # Simple logic for chatbot responses
    

# Adding a message handler to catch text messages
respond_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, respond)
app.add_handler(respond_handler)

# Handle unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Log unknown command to terminal
    print(f"Unknown command received from {update.effective_user.username}: {update.message.text}")
    
    await update.message.reply_text("Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(filters.COMMAND, unknown)
app.add_handler(unknown_handler)

# To start the bot
if __name__ == '__main__':
    print("The bot is starting...")
    app.run_polling()
    print("The bot is stopped.")