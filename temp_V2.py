import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the states for the conversation
BRANCH, SEMESTER, SUBJECT, UNIT , BRANCH2 = range(5)

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
    branch_buttons = [
        [InlineKeyboardButton("CS", callback_data="CS")],
        [InlineKeyboardButton("IS", callback_data="IS")]
    ]
    reply_markup = InlineKeyboardMarkup(branch_buttons)

    update.message.reply_text('Welcome! Please select your branch:', reply_markup=reply_markup)

    return BRANCH

# Handler for the branch selection
def select_branch2(update, context):
    query = update.callback_query
    context.user_data['branch'] = query.data

    semester_buttons = [
        [InlineKeyboardButton("1", callback_data="1"),
         InlineKeyboardButton("2", callback_data="2")]
        # Add more semesters if needed
    ]
    reply_markup = InlineKeyboardMarkup(semester_buttons)

    query.edit_message_text(text=f'You selected {context.user_data["branch"]}. Please select your semester:',
                            reply_markup=reply_markup)

    return SEMESTER

def select_branch(update, context):
    query = update.callback_query
    context.user_data['branch'] = query.data

    semester_buttons = [
        [InlineKeyboardButton("1", callback_data="1"),
         InlineKeyboardButton("2", callback_data="2")]
        # Add more semesters if needed
    ]
    reply_markup = InlineKeyboardMarkup(semester_buttons)

    query.edit_message_text(text=f'You selected {context.user_data["branch"]}. Please select your semester:',
                            reply_markup=reply_markup)

    return SEMESTER

# Handler for the semester selection
def select_semester(update, context):
    query = update.callback_query
    context.user_data['semester'] = query.data

    subject_buttons = []
    branch = context.user_data['branch']
    semester = context.user_data['semester']
    if branch in subjects and semester in subjects[branch]:
        semester_subjects = subjects[branch][semester]
        for subject in semester_subjects:
            subject_buttons.append([InlineKeyboardButton(subject, callback_data=subject)])

    reply_markup = InlineKeyboardMarkup(subject_buttons)

    query.edit_message_text(text=f'You selected {context.user_data["branch"]} branch and semester {context.user_data["semester"]}. '
                                 f'Please select a subject:',
                            reply_markup=reply_markup)

    return SUBJECT

# Handler for subject selection
def select_subject(update, context):
    query = update.callback_query
    context.user_data['subject'] = query.data

    unit_buttons = [
        [InlineKeyboardButton("Unit 1", callback_data="unit_1"),
         InlineKeyboardButton("Unit 2", callback_data="unit_2")],
        [InlineKeyboardButton("Unit 3", callback_data="unit_3"),
         InlineKeyboardButton("Unit 4", callback_data="unit_4"),
         InlineKeyboardButton("Unit 5", callback_data="unit_5")]
    ]
    reply_markup = InlineKeyboardMarkup(unit_buttons)

    query.edit_message_text(text=f'You selected {context.user_data["subject"]}. '
                                 f'Please select the unit:',
                            reply_markup=reply_markup)

    return UNIT

# Handler for unit selection
def select_unit(update, context):
    query = update.callback_query
    context.user_data['unit'] = query.data

    branch = context.user_data['branch']
    semester = context.user_data['semester']
    subject = context.user_data['subject']
    unit = context.user_data['unit']

    file_name = f'{branch}_{semester}_{subject}_{unit}.pdf'
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    if os.path.exists(file_path):
        # Send the PDF file
        update.effective_message.reply_document(document=open(file_path, 'rb'))
        update.effective_message.reply_text('PDF sent successfully!')
    else:
        update.effective_message.reply_text('PDF file not found.')

    # Reset the conversation state
    context.user_data.clear()
    branch_buttons = [
        [InlineKeyboardButton("CS", callback_data="CS")],
        [InlineKeyboardButton("IS", callback_data="IS")]
    ]
    reply_markup = InlineKeyboardMarkup(branch_buttons)

    update.effective_message.reply_text(text=f'ok',
                            reply_markup=reply_markup)
    return BRANCH2

# Handler for canceling the conversation
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('The conversation has been canceled. Goodbye!')

    return ConversationHandler.END

# Main function to start the bot
def main():
    # Create the EventHandler and pass it your bot's token
    updater = Updater("6052177187:AAFZOl3I4Ftj1iN8uRrSp92D2VitkH3aYlE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            BRANCH: [CallbackQueryHandler(select_branch, pattern='^(CS|IS)$')],
            SEMESTER: [CallbackQueryHandler(select_semester)],
            SUBJECT: [CallbackQueryHandler(select_subject)],
            UNIT: [CallbackQueryHandler(select_unit)] , 
            BRANCH2:[CallbackQueryHandler(select_branch2)]
        } ,
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
