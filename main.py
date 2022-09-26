import logging
import pymysql
import re
import pathlib
from dotenv import load_dotenv
import os

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Connect database with chatbot and move on to chatbot database
db = pymysql.connect(host="localhost", user="root", charset="utf8")
cursor = db.cursor()
cursor.execute('USE chatbot;')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

QUESTION_1, QUESTION_2, QUESTION_3, QUESTION_4 = range(4)

async def discussion (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    args = (update.message.chat.id, context.user_data["question_id"], user.first_name, update.message.text)

    logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    db.commit()

    if context.user_data["question_id"] == 1:
        return QUESTION_1
    elif context.user_data["question_id"] == 2:
        return QUESTION_2

async def question_1 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_photo(
        open('P-1-1.png', 'rb')
    )

    await update.message.reply_photo(
        open('P-1-2.png', 'rb')
    )

    await update.message.reply_photo(
        open('P-1-3.png', 'rb')
    )

    context.user_data["question_id"] = 1

    return QUESTION_1


async def question_1_answer_right(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    args = (update.message.chat.id, 1, user.first_name, update.message.text)

    logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    db.commit()
    await update.message.reply_photo(
        open('S-1-1.png', 'rb')
    )

    await update.message.reply_photo(
        open('P-2-1.png', 'rb')
    )

    await update.message.reply_photo(
        open('P-2-2.png', 'rb')
    )

    await update.message.reply_photo(
        open('P-1-3.png', 'rb')
    )

    context.user_data["question_id"] = 2

    return QUESTION_2

async def question_1_answer_wrong(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    args = (update.message.chat.id, 1, user.first_name, update.message.text)

    logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    db.commit()

    await update.message.reply_photo(
        open('S-1-2.png', 'rb')
    )

    await update.message.reply_photo(
        open('S-1-3.png', 'rb')
    )

    await update.message.reply_photo(
        open('P-2-1.png', 'rb')
    )

    await update.message.reply_photo(
        open('P-2-2.png', 'rb')
    )

    await update.message.reply_photo(
        open('P-1-3.png', 'rb')
    )

    context.user_data["question_id"] = 2

    return QUESTION_2

async def question_2_answer_right(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    args = (update.message.chat.id, 2, user.first_name, update.message.text)

    logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    db.commit()

    await update.message.reply_photo(
        open('S-1-1.png', 'rb')
    )

    return QUESTION_3

async def question_2_answer_wrong(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    args = (update.message.chat.id, 2, user.first_name, update.message.text)

    logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    db.commit()

    await update.message.reply_photo(
        open('S-2-2.png', 'rb')
    )

    return QUESTION_3

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

if __name__ == '__main__':
    load_dotenv()
    application = Application.builder().token(os.environ.get('telegram-bot-token')).build()
    
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", question_1)],
        states={
            QUESTION_1 : [
                MessageHandler(filters.Regex("^[^답\s*:\s*]"), discussion),
                MessageHandler(filters.Regex("^답\s*:\s*5($|[^\u0030-\u0039])"), question_1_answer_right),
                MessageHandler(filters.Regex("^답\s*:\s*([^5]|5[0-9])"), question_1_answer_wrong)
            ],
            QUESTION_2: [
                MessageHandler(filters.Regex("^[^답\s*:\s*]"), discussion),
                MessageHandler(filters.Regex("^답\s*:\s*500($|[^\u0030-\u0039])"), question_2_answer_right),
                MessageHandler(filters.Regex("^답\s*:\s*(?!(?:500))(\d+|\D+)"), question_2_answer_wrong),
            ],

            QUESTION_3: [
                MessageHandler(filters.Regex("^[^답\s*:\s*]"), discussion),
                MessageHandler(filters.Regex("^답\s*:\s*1500($|[^\u0030-\u0039])"), question_2_answer_right),
                MessageHandler(filters.Regex("^답\s*:\s*1500($|[^\u0030-\u0039])"), question_2_answer_wrong),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
