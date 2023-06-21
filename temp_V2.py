import logging
import os
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

# Enable loggingṇ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the states for the conversation
NAME, USN, SEMESTER, SUBJECT, UNIT = range(5)

# Define the subjects for each branch and semester
subjects = {
    'CS': {
        '1': ['Subject 1', 'Subject 2'],
        '2': ['Subject 3', 'Subject 4'],
        # Add subjects for other semesters
    },
    'IS': {
        '1': ['Subject 5', 'Subject 6'],
        '2': ['Subject 7', 'Subject 8'],
        # Add subjects for other semesters
    }
}

# Handler for the /start command
def start(update, context):
    user_id = str(update.effective_user.id)
    context.user_data[user_id] = {}

    update.message.reply_text('Welcome! Please enter your name:')
    return NAME

def collect_name(update, context):
    user_id = str(update.effective_user.id)
    context.user_data[user_id]['name'] = update.message.text
    
    update.message.reply_text('Please enter your USN (University Seat Number):')
    
    return USN


# Handler for validating the USN format
def validate_usn(update, context):
    user_id = str(update.effective_user.id)
    usn = update.message.text.upper()  # Convert to uppercase for case insensitivity
    query = update.callback_query    
    # Define the regular expression pattern for the USN format
    pattern = r'^\dSI\d{2}(CS|IS|AI|EC|EE)\d{3}$'
    
    if re.match(pattern, usn):
        context.user_data[user_id]['usn'] = usn
        branch_from_usn = usn[5:7]
        print(branch_from_usn)
        context.user_data[user_id]['branch'] = branch_from_usn
        semester_buttons = [
            [InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2")]
            # Add more semesters if needed
        ]
        reply_markup = InlineKeyboardMarkup(semester_buttons)
        update.effective_message.reply_text(text=f'You selected {context.user_data[user_id]["branch"]}. Please select your semester:',
                            reply_markup=reply_markup)

        return SEMESTER
    else:
        update.message.reply_text('Invalid USN format! Please try again.')
        return USN

# Handler for the semester selection
def select_semester(update, context):
    query = update.callback_query
    user_id = str(query.from_user.id)
    context.user_data[user_id]['semester'] = query.data

    subject_buttons = []
    branch = context.user_data[user_id]['branch']
    semester = context.user_data[user_id]['semester']
    if branch in subjects and semester in subjects[branch]:
        semester_subjects = subjects[branch][semester]
        for subject in semester_subjects:
            subject_buttons.append([InlineKeyboardButton(subject, callback_data=subject)])

    reply_markup = InlineKeyboardMarkup(subject_buttons + [[InlineKeyboardButton("Go Back", callback_data="go_back")]])

    query.edit_message_text(text=f'You selected {context.user_data[user_id]["branch"]} branch and semester {context.user_data[user_id]["semester"]}. '
                                 f'Please select a subject:',
                            reply_markup=reply_markup)

    return SUBJECT

# Handler for subject selection
def select_subject(update, context):
    query = update.callback_query
    user_id = str(query.from_user.id)
    if query.data == 'go_back':
        semester_buttons = [
            [InlineKeyboardButton("1", callback_data="1"),
             InlineKeyboardButton("2", callback_data="2")]
        # Add more semesters if needed
        ]
        reply_markup = InlineKeyboardMarkup(semester_buttons)
        query.edit_message_text(text=f'You selected {context.user_data[user_id]["branch"]}. Please select your semester:',
                            reply_markup=reply_markup)
        return SEMESTER

    context.user_data[user_id]['subject'] = query.data

    unit_buttons = [
        [InlineKeyboardButton("Unit 1", callback_data="unit_1"),
         InlineKeyboardButton("Unit 2", callback_data="unit_2")],
        [InlineKeyboardButton("Unit 3", callback_data="unit_3"),
         InlineKeyboardButton("Unit 4", callback_data="unit_4"),
         InlineKeyboardButton("Unit 5", callback_data="unit_5")],
        [InlineKeyboardButton("Go Back", callback_data="go_back_subject")]
    ]
    reply_markup = InlineKeyboardMarkup(unit_buttons)

    query.edit_message_text(text=f'You selected {context.user_data[user_id]["subject"]}. '
                                 f'Please select the unit:',
                            reply_markup=reply_markup)

    return UNIT

# Handler for unit selection
def select_unit(update, context):
    query = update.callback_query
    user_id = str(query.from_user.id)
    if query.data == 'go_back_subject':
        subject_buttons = []
        branch = context.user_data[user_id]['branch']
        semester = context.user_data[user_id]['semester']
        if branch in subjects and semester in subjects[branch]:
            semester_subjects = subjects[branch][semester]
            for subject in semester_subjects:
                subject_buttons.append([InlineKeyboardButton(subject, callback_data=subject)])

        reply_markup = InlineKeyboardMarkup(subject_buttons + [[InlineKeyboardButton("Go Back", callback_data="go_back")]])
        query.edit_message_text(text=f'You selected {context.user_data[user_id]["branch"]} branch and semester {context.user_data[user_id]["semester"]}. '
                                 f'Please select a subject:',
                            reply_markup=reply_markup)

        return SUBJECT
    context.user_data[user_id]['unit'] = query.data
    branch = context.user_data[user_id]['branch']
    semester = context.user_data[user_id]['semester']
    subject = context.user_data[user_id]['subject']
    unit = context.user_data[user_id]['unit']

    file_name = f'{branch}_{semester}_{subject}_{unit}.pdf'
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    if os.path.exists(file_path):
        # Send the PDF file
        update.effective_message.reply_document(document=open(file_path, 'rb'))
        update.effective_message.reply_text('PDF sent successfully!')
    else:
        update.effective_message.reply_text('PDF file not found.')

    subject_buttons = []
    branch = context.user_data[user_id]['branch']
    semester = context.user_data[user_id]['semester']
    if branch in subjects and semester in subjects[branch]:
        semester_subjects = subjects[branch][semester]
        for subject in semester_subjects:
            subject_buttons.append([InlineKeyboardButton(subject, callback_data=subject)])

    reply_markup = InlineKeyboardMarkup(subject_buttons + [[InlineKeyboardButton("Go Back", callback_data="go_back")]])

    update.effective_message.reply_text(text=f'You selected {context.user_data[user_id]["branch"]} branch and semester {context.user_data[user_id]["semester"]}. '
                                              f'Please select a subject:',
                                        reply_markup=reply_markup)

    return SUBJECT


# Handler for unknown commands
# def unknown(update, context):
#     user_id = str(update.effective_user.id)
#     if user_id in context.user_data:
#         del context.user_data[user_id]
#     update.message.reply_text('Unknown command! Please try again.')

# Handler for canceling the conversation
def cancel(update, context):
    update.message.reply_text('Conversation canceled.')
    return ConversationHandler.END

# Main function
def main():
    # Get the Telegram bot token from an environment variable
    token = '6052177187:AAFZOl3I4Ftj1iN8uRrSp92D2VitkH3aYlE'

    if token is None:
        print('Please set the TELEGRAM_BOT_TOKEN environment variable.')
        return

    # Create the Updater and dispatcher
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Create the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            NAME: [MessageHandler(Filters.text, collect_name)],
            USN: [MessageHandler(Filters.text, validate_usn)],
            SEMESTER: [CallbackQueryHandler(select_semester)],
            SUBJECT: [CallbackQueryHandler(select_subject)],
            UNIT: [CallbackQueryHandler(select_unit)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add the conversation handler to the dispatcher
    dp.add_handler(conv_handler)

    # Add handler for unknown commands
    # dp.add_handler(MessageHandler(Filters.command, unknown))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
