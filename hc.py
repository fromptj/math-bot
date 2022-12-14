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
from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
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

# QUESTION 1 : 1 / QUESTION 2 : 3 / QUESTION 3 : 5 / QUESTION 4 : 7 / QUESTION 5 : 9
START, QUESTION_1, QUESTION_1_ADDED, QUESTION_2, QUESTION_2_ADDED, QUESTION_3, QUESTION_3_ADDED, QUESTION_4, QUESTION_4_ADDED, QUESTION_5, QUESTION_5_ADDED, \
QUESTION_6, QUESTION_6_ADDED, QUESTION_7, QUESTION_7_ADDED, QUESTION_8, QUESTION_8_ADDED, QUESTION_9, QUESTION_9_ADDED, QUESTION_10, QUESTION_10_ADDED, \
QUESTION_11, QUESTION_11_ADDED, QUESTION_12, QUESTION_12_ADDED, QUESTION_13, QUESTION_13_ADDED, QUESTION_14, QUESTION_14_ADDED, QUESTION_15, QUESTION_15_ADDED = range(31)

async def explanation (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    chat_id = update.message.chat.id

    args = (chat_id, "hc", context.user_data["question_id"], user.id, update.message.text)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, cond, question_id, user_id, explanation) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    return 2 * context.user_data["question_id"]


async def start (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="안녕 반가워! 나는 오늘 너와 함께 공부할 챗봇이야.\n내가 문제 15개를 풀었는데, 내 답이 맞았는지 틀렸는지에 대해 조언을 부탁할게!"
    )

    start_button = [[InlineKeyboardButton('준비됐어', callback_data='준비됐어')]]

    reply_markup = InlineKeyboardMarkup(start_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text='공부할 준비가 되면 아래 보이는 <준비됐어> 버튼을 눌러줘!',
        reply_markup=reply_markup
    )

    return START

async def question_1 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그럼 1번 문제부터 시작해보자!',
    )

    await context.bot.send_photo(
        chat_id, open('c1.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 답은 16×14÷2야.\n\n내가 구한 답이 맞니?",
        reply_markup= reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 1

    return QUESTION_1


async def question_1_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 1, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_1_ADDED

async def question_1_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 1, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_1_ADDED

async def question_2 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 2번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c2.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="답을 구해보니, (90×60)÷2가 나왔어.\n\n내가 구한 게 정답이니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 2

    return QUESTION_2

async def question_2_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 2, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_2_ADDED

async def question_2_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 2, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_2_ADDED

async def question_3 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 3번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c3.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답은 (200+60)×140÷2야.\n\n내가 구한 답 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 3

    return QUESTION_3

async def question_3_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 3, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_3_ADDED

async def question_3_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 3, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_3_ADDED

async def question_4 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 4번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c4.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 답이 15×8이라고 생각해.\n\n내 답이 맞을까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 4

    return QUESTION_4

async def question_4_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 4, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_4_ADDED

async def question_4_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 4, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_4_ADDED

async def question_5 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 5번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c5.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 400×630이야.\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 5

    return QUESTION_5

async def question_5_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 5, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_5_ADDED

async def question_5_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 5, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_5_ADDED


async def question_6 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 6번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c6.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 답은 7×9야.\n\n내가 구한 답이 맞니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 6

    return QUESTION_6


async def question_6_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 6, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_6_ADDED

async def question_6_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 6, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_6_ADDED

async def question_7 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 7번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c7.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="답을 구해보니, 18×18÷2가 나왔어.\n\n내가 구한 게 정답이니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 7

    return QUESTION_7

async def question_7_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 7, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_7_ADDED

async def question_7_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 7, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_7_ADDED

async def question_8 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 8번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c8.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 40×50이야.\n\n내가 구한 답 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 8

    return QUESTION_8

async def question_8_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 8, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_8_ADDED

async def question_8_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 8, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_8_ADDED

async def question_9 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 9번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c9.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 답이 35×35라고 생각해.\n\n내 답이 맞을까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 9

    return QUESTION_9

async def question_9_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 9, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_9_ADDED

async def question_9_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 9, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_9_ADDED

async def question_10 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 10번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c10.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 (15+9)×7÷2야.\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 10

    return QUESTION_10

async def question_10_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 10, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_10_ADDED

async def question_10_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 10, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_10_ADDED

async def question_11 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 11번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c11.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 105×68야.\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 11

    return QUESTION_11

async def question_11_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 11, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_11_ADDED

async def question_11_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 11, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_11_ADDED

async def question_12 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 12번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c12.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="답을 구해보니, 7×12÷2가 나왔어.\n\n내가 구한 게 정답이니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 12

    return QUESTION_12

async def question_12_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 12, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_12_ADDED

async def question_12_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 12, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_12_ADDED

async def question_13 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 13번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c13.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 30×60이야.\n\n내가 구한 답 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 13

    return QUESTION_13

async def question_13_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 13, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_13_ADDED

async def question_13_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 13, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_13_ADDED

async def question_14 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 14번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c14.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 답이 (5+15)×6÷2라고 생각해.\n\n내 답이 맞을까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 14

    return QUESTION_14

async def question_14_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 14, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_14_ADDED

async def question_14_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 14, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_14_ADDED

async def question_15 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음은 15번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c15.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 (4×6)÷2야.\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 15

    return QUESTION_15

async def question_15_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 15, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n어떻게 답이 나왔는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_15_ADDED

async def question_15_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    args = (chat_id, update.callback_query.data, "hc", 15, user.id)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n왜 틀렸는지 설명해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_15_ADDED

async def end (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="오늘 준비한 수학 문제는 여기까지야!\n다음에 또 같이 공부하자ㅎㅎ 오늘 함께해줘서 고마워~"
    )

    return ConversationHandler.END

async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    if not context.user_data:
        context.user_data["question_id"] = 1

    callback_number = 2 * context.user_data["question_id"] - 1

    await context.bot.send_message(
        chat_id=chat_id, text="버튼을 눌러서 알려줘!"
    )

    return callback_number


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    return ConversationHandler.END
"""
def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    # Remove job with given name. Returns whether job was removed.
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def callback_second(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=context.job.chat_id, photo=context.job.data)
"""

if __name__ == '__main__':
    load_dotenv()
    application = Application.builder().token(os.environ.get('hc_math_bot')).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [
                CallbackQueryHandler(question_1, pattern="^\s*준비됐어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
                # MessageHandler(filters.Regex("^\s*준비됐어\s*"), question_1),
                #MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_1: [
                CallbackQueryHandler(question_1_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_1_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_1_ADDED: [
                CallbackQueryHandler(question_2, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_2: [
                CallbackQueryHandler(question_2_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_2_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_2_ADDED: [
                CallbackQueryHandler(question_3, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_3: [
                CallbackQueryHandler(question_3_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_3_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_3_ADDED: [
                CallbackQueryHandler(question_4, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_4: [
                CallbackQueryHandler(question_4_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_4_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_4_ADDED: [
                CallbackQueryHandler(question_5, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_5: [
                CallbackQueryHandler(question_5_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_5_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_5_ADDED: [
                CallbackQueryHandler(question_6, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_6: [
                CallbackQueryHandler(question_6_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_6_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_6_ADDED: [
                CallbackQueryHandler(question_7, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_7: [
                CallbackQueryHandler(question_7_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_7_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_7_ADDED: [
                CallbackQueryHandler(question_8, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_8: [
                CallbackQueryHandler(question_8_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_8_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_8_ADDED: [
                CallbackQueryHandler(question_9, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_9: [
                CallbackQueryHandler(question_9_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_9_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_9_ADDED: [
                CallbackQueryHandler(question_10, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_10: [
                CallbackQueryHandler(question_10_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_10_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_10_ADDED: [
                CallbackQueryHandler(question_11, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_11: [
                CallbackQueryHandler(question_11_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_11_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_11_ADDED: [
                CallbackQueryHandler(question_12, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_12: [
                CallbackQueryHandler(question_12_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_12_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_12_ADDED: [
                CallbackQueryHandler(question_13, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_13: [
                CallbackQueryHandler(question_13_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_13_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_13_ADDED: [
                CallbackQueryHandler(question_14, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_14: [
                CallbackQueryHandler(question_14_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_14_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_14_ADDED: [
                CallbackQueryHandler(question_15, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_15: [
                CallbackQueryHandler(question_15_answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(question_15_answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_15_ADDED: [
                CallbackQueryHandler(end, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
