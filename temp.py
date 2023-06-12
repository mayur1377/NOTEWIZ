import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telegram.Bot(token='6052177187:AAFZOl3I4Ftj1iN8uRrSp92D2VitkH3aYlE')

def start(update, context):
    # Create a list of subject buttons
    subject_button_list = [
        [InlineKeyboardButton("DBMS", callback_data='dbms')],
        [InlineKeyboardButton("OS", callback_data='os')],
        [InlineKeyboardButton("OOPS", callback_data='oops')],
        [InlineKeyboardButton("Java", callback_data='java')],
        [InlineKeyboardButton("DSA", callback_data='dsa')]
    ]

    # Create an InlineKeyboardMarkup with the subject button list
    reply_markup = InlineKeyboardMarkup(subject_button_list)

    # Send a message with the subject button list to the user
    update.message.reply_text("Please select a subject:", reply_markup=reply_markup)

def subject_click(update, context):
    query = update.callback_query
    subject = query.data

    # Store the selected subject in the user's context
    context.user_data['subject'] = subject

    # Create a list of unit buttons for the selected subject
    unit_button_list = [
        [InlineKeyboardButton("Unit 1", callback_data='unit1')],
        [InlineKeyboardButton("Unit 2", callback_data='unit2')],
        [InlineKeyboardButton("Unit 3", callback_data='unit3')],
        [InlineKeyboardButton("Unit 4", callback_data='unit4')],
        [InlineKeyboardButton("Unit 5", callback_data='unit5')]
    ]

    # Create an InlineKeyboardMarkup with the unit button list
    reply_markup = InlineKeyboardMarkup(unit_button_list)

    # Send a message with the unit button list to the user
    query.message.reply_text(f"Please select a unit for {subject}:", reply_markup=reply_markup)

def unit_click(update, context):
    query = update.callback_query
    unit = query.data

    # Retrieve the selected subject from the user's context
    subject = context.user_data.get('subject')

    # Send the corresponding PDF file based on the subject and unit selected
    pdf_path = f"{subject}_{unit}.pdf"
    with open(pdf_path, 'rb') as pdf_file:
        query.message.reply_document(pdf_file)

# Handler for the /start command
start_handler = CommandHandler('start', start)
# Handler for subject button clicks
subject_handler = CallbackQueryHandler(subject_click, pattern='^(dbms|os|oops|java|dsa)$')
# Handler for unit button clicks
unit_handler = CallbackQueryHandler(unit_click, pattern='^unit[1-5]$')

# Create the updater and add the handlers to it
updater = Updater('6052177187:AAFZOl3I4Ftj1iN8uRrSp92D2VitkH3aYlE', use_context=True)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(subject_handler)
updater.dispatcher.add_handler(unit_handler)

# Start the bot
updater.start_polling()
