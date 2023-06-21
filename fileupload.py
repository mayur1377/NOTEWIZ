import os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Define a handler for the /start command
def start(update, context):
    update.message.reply_text("Please upload a file.")

# Define a handler for file uploads
def handle_file_upload(update, context):
    user_id = update.message.from_user.id
    file = update.message.document
    file_id = file.file_id
    file_name = file.file_name

    # Get the current working directory
    current_dir = os.getcwd()

    # Save the file to the server
    file_path = os.path.join(current_dir, file_name)
    context.bot.get_file(file_id).download(file_path)

    # You can further process or use the saved file as needed

    # Reply to the user with a confirmation message
    update.message.reply_text(f"File '{file_name}' has been saved to the server.")

# Create the Telegram bot
updater = Updater("6020885932:AAFbsMkii0xDibWQ8oPIrNUJtRwKpcVUalU", use_context=True)
dispatcher = updater.dispatcher

# Add the handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.document, handle_file_upload))

# Start the bot
updater.start_polling()
