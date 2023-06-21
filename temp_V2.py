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
NAME, USN, SEMESTER, SUBJECT, UNIT , TEACHER = range(6)

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
# Handler for the /start command
def start(update, context):
    user_id = str(update.effective_user.id)
    if user_id in context.user_data:
        # User already exists, skip initial prompts
        update.message.reply_text('Please enter your name:')
        return NAME
    # New user, initiate conversation
    context.user_data[user_id] = {}
    update.message.reply_text('Welcome! Please enter your name:')
    return NAME

def collect_name(update, context):
    user_id = str(update.effective_user.id)
    name = update.message.text.strip()  # Remove leading/trailing whitespace
    context.user_data[user_id]['name'] = name
    # Define the regular expression pattern for the name format
    pattern = r'^[a-zA-Z]{4,}$'
    if re.match(pattern, name):
        if name.lower() == 'mayur':
            update.message.reply_text('welcome to teacher mode , upload a pdf')
            return TEACHER
        else:
            update.message.reply_text('Please enter your USN (University Seat Number):')
            return USN
    else:
        update.message.reply_text('Dosent seem like a valid name , please try again')
        return NAME




# Handler for validating the USN format
# Handler for validating the USN format
def validate_usn(update, context):
    user_id = str(update.effective_user.id)
    usn = update.message.text.upper()  # Convert to uppercase for case insensitivity
    query = update.callback_query
    pattern = r'^\dSI\d{2}(CS|IS|AI|EC|EE)\d{3}$'

    if re.match(pattern, usn):
        # Check if USN already exists in user data
        for user_data in context.user_data.values():
            if 'usn' in user_data and user_data['usn'] == usn:
                update.message.reply_text('USN already exists. Please enter your usn.')
                return USN

        # USN is valid and not a duplicate
        context.user_data[user_id]['usn'] = usn
        branch_from_usn = usn[5:7]
        context.user_data[user_id]['branch'] = branch_from_usn
        semester_buttons = [
        [InlineKeyboardButton("SEM I", callback_data="1")],
        [InlineKeyboardButton("SEM II", callback_data="2")],
        [InlineKeyboardButton("SEM III", callback_data="3")] , 
        [InlineKeyboardButton("SEM IV", callback_data="4")] , 
        [InlineKeyboardButton("SEM V", callback_data="5")] , 
        [InlineKeyboardButton("SEM VI", callback_data="6")] , 
        [InlineKeyboardButton("SEM VII", callback_data="7")],
        [InlineKeyboardButton("SEM VIII", callback_data="8")]]
        # Add more semesters if needed
        reply_markup = InlineKeyboardMarkup(semester_buttons)
        update.effective_message.reply_text(text=f'USN validated. Please select your semester:',
                                            reply_markup=reply_markup)
        return SEMESTER
    else:
        update.message.reply_text('Invalid USN format! Please try again.')
        return USN


def teacher(update, context):
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

    query.edit_message_text(text=f'{context.user_data[user_id]["branch"]} branch and semester {context.user_data[user_id]["semester"]}. '
                                 f'Please select a subject:',
                            reply_markup=reply_markup)

    return SUBJECT

# Handler for subject selection
def select_subject(update, context):
    query = update.callback_query
    user_id = str(query.from_user.id)
    if query.data == 'go_back':
        semester_buttons = [
        [InlineKeyboardButton("SEM I", callback_data="1")],
        [InlineKeyboardButton("SEM II", callback_data="2")],
        [InlineKeyboardButton("SEM III", callback_data="3")] , 
        [InlineKeyboardButton("SEM IV", callback_data="4")] , 
        [InlineKeyboardButton("SEM V", callback_data="5")] , 
        [InlineKeyboardButton("SEM VI", callback_data="6")] , 
        [InlineKeyboardButton("SEM VII", callback_data="7")],
        [InlineKeyboardButton("SEM VIII", callback_data="8")]]
        # Add more semesters if needed
        reply_markup = InlineKeyboardMarkup(semester_buttons)
        query.edit_message_text(text=f'Please select your semester:',
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
    name =context.user_data[user_id]['name']

    file_name = f'{branch}_{semester}_{subject}_{unit}.pdf'
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    if os.path.exists(file_path):
    # Send the PDF file
        update.effective_message.reply_document(document=open(file_path, 'rb'))
        query.edit_message_text(f'HERE YOU GO {name} ! {subject} Unit {unit} successfully!')
    else:
        query.edit_message_text('PDF file not found.')

    subject_buttons = []
    branch = context.user_data[user_id]['branch']
    semester = context.user_data[user_id]['semester']
    if branch in subjects and semester in subjects[branch]:
        semester_subjects = subjects[branch][semester]
        for subject in semester_subjects:
            subject_buttons.append([InlineKeyboardButton(subject, callback_data=subject)])

    reply_markup = InlineKeyboardMarkup(subject_buttons + [[InlineKeyboardButton("Go Back", callback_data="go_back")]])

    update.effective_message.reply_text(text=f'Please select the next subject you wanna study from:',
                                        reply_markup=reply_markup)

    return SUBJECT


# Handler for unknown commands
def unknown(update, context):
    user_id = str(update.effective_user.id)
    if user_id in context.user_data:
        del context.user_data[user_id]
    update.message.reply_text('Unknown command! Please try again.')

# Handler for canceling the conversation
def cancel(update, context):
    update.message.reply_text('Conversation canceled.')

# Main function
def main():
    # Get the Telegram bot token from an environment variable
    token = '6020885932:AAFbsMkii0xDibWQ8oPIrNUJtRwKpcVUalU'

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
            TEACHER: [CallbackQueryHandler(teacher)],
        },

        fallbacks=[]
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
