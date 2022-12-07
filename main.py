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
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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

# QUESTION 1 : 1 / QUESTION 2 : 4 / QUESTION 3 : 7 / QUESTION 4 : 10 / QUESTION 5 : 13
# NAVIGATION 1 : 3 / NAVIGATION 2 : 6 / NAVIGATION 3 : 9 / NAVIGATION 3 : 12 / NAVIGATION 3 : 15
START, QUESTION_1, QUESTION_1_ADDED, NAVIGATION_1, QUESTION_2, QUESTION_2_ADDED, NAVIGATION_2, QUESTION_3, QUESTION_3_ADDED, NAVIGATION_3, QUESTION_4, QUESTION_4_ADDED, NAVIGATION_4, QUESTION_5, QUESTION_5_ADDED, NAVIGATION_5 = range(16)

async def explanation (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    args = (update.message.chat.id, context.user_data["question_id"], user.first_name, update.message.text)

    logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    db.commit()

    if context.user_data["question_id"] == 1:
        return QUESTION_1_ADDED
    elif context.user_data["question_id"] == 2:
        return QUESTION_2_ADDED
    elif context.user_data["question_id"] == 3:
        return QUESTION_3_ADDED
    elif context.user_data["question_id"] == 4:
        return QUESTION_4_ADDED
    elif context.user_data["question_id"] == 5:
        return QUESTION_5_ADDED

async def start (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="안녕 반가워! 나는 오늘 너와 함께 공부할 챗봇이야.\n내가 문제 10개를 풀었는데, 내 답이 맞았는지 틀렸는지에 대해 조언을 부탁할게!"
    )

    start_button = [[KeyboardButton('준비됐어!')]]

    reply_markup = ReplyKeyboardMarkup(start_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text='공부할 준비가 되면 아래 보이는 <준비됐어> 버튼을 눌러줘!',
        reply_markup=reply_markup
    )

    return START

async def question_1 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그럼 1번 문제부터 시작해보자!',
    )

    await context.bot.send_photo(
        update.message.chat.id, open('c1.png', 'rb')
    )

    ox_button = [[KeyboardButton('맞아')], [KeyboardButton('틀렸어')]]
    reply_markup = ReplyKeyboardMarkup(ox_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 답은 16×14÷2야.\n\n내가 구한 답이 맞니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 1

    return QUESTION_1


async def question_1_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    chat_id = update.message.chat.id

    #args = (update.message.chat.id, 1, user.first_name, update.message.text)
    #logger.info("Answer of %s: %s", user.first_name, update.message.text)
    #cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    #db.commit()

    submit_button = [[KeyboardButton('제출하기')]]
    reply_markup = ReplyKeyboardMarkup(submit_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n혹시 내가 구한 답에 덧붙일 내용이 있으면 말해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_1_ADDED

async def question_1_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    chat_id = update.message.chat.id

    #args = (update.message.chat.id, 1, user.first_name, update.message.text)
    #logger.info("Answer of %s: %s", user.first_name, update.message.text)
    #cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    #db.commit()

    submit_button = [[KeyboardButton('제출하기')]]
    reply_markup = ReplyKeyboardMarkup(submit_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n혹시 내가 구한 답에 덧붙일 내용이 있으면 말해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_1_ADDED

async def question_2 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음은 2번 문제야!',
    )

    await context.bot.send_photo(
        update.message.chat.id, open('c2.png', 'rb')
    )

    ox_button = [[KeyboardButton('맞아')], [KeyboardButton('틀렸어')]]
    reply_markup = ReplyKeyboardMarkup(ox_button, one_time_keyboard=True)

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
    user = update.message.from_user
    chat_id = update.message.chat.id

    #args = (update.message.chat.id, 1, user.first_name, update.message.text)
    #logger.info("Answer of %s: %s", user.first_name, update.message.text)
    #cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    #db.commit()

    submit_button = [[KeyboardButton('제출하기')]]
    reply_markup = ReplyKeyboardMarkup(submit_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n혹시 내가 구한 답에 덧붙일 내용이 있으면 말해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_2_ADDED

async def question_2_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    chat_id = update.message.chat.id

    #args = (update.message.chat.id, 1, user.first_name, update.message.text)
    #logger.info("Answer of %s: %s", user.first_name, update.message.text)
    #cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    #db.commit()

    submit_button = [[KeyboardButton('제출하기')]]
    reply_markup = ReplyKeyboardMarkup(submit_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n혹시 내가 구한 답에 덧붙일 내용이 있으면 말해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_2_ADDED

async def question_3 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='이제 3번 문제야',
    )

    await context.bot.send_photo(
        update.message.chat.id, open('c3.png', 'rb')
    )

    ox_button = [[KeyboardButton('맞아')], [KeyboardButton('틀렸어')]]
    reply_markup = ReplyKeyboardMarkup(ox_button, one_time_keyboard=True)

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
    user = update.message.from_user
    chat_id = update.message.chat.id

    #args = (update.message.chat.id, 1, user.first_name, update.message.text)
    #logger.info("Answer of %s: %s", user.first_name, update.message.text)
    #cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    #db.commit()

    submit_button = [[KeyboardButton('제출하기')]]
    reply_markup = ReplyKeyboardMarkup(submit_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n혹시 내가 구한 답에 덧붙일 내용이 있으면 말해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_3_ADDED

async def question_3_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    chat_id = update.message.chat.id

    #args = (update.message.chat.id, 1, user.first_name, update.message.text)
    #logger.info("Answer of %s: %s", user.first_name, update.message.text)
    #cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    #db.commit()

    submit_button = [[KeyboardButton('제출하기')]]
    reply_markup = ReplyKeyboardMarkup(submit_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n혹시 내가 구한 답에 덧붙일 내용이 있으면 말해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_3_ADDED

async def question_4 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='4번 문제로 넘어가보자!',
    )

    await context.bot.send_photo(
        update.message.chat.id, open('c4.png', 'rb')
    )

    ox_button = [[KeyboardButton('맞아')], [KeyboardButton('틀렸어')]]
    reply_markup = ReplyKeyboardMarkup(ox_button, one_time_keyboard=True)

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
    user = update.message.from_user
    chat_id = update.message.chat.id

    #args = (update.message.chat.id, 1, user.first_name, update.message.text)
    #logger.info("Answer of %s: %s", user.first_name, update.message.text)
    #cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    #db.commit()

    submit_button = [[KeyboardButton('제출하기')]]
    reply_markup = ReplyKeyboardMarkup(submit_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n혹시 내가 구한 답에 덧붙일 내용이 있으면 말해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_4_ADDED

async def question_4_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    chat_id = update.message.chat.id

    #args = (update.message.chat.id, 1, user.first_name, update.message.text)
    #logger.info("Answer of %s: %s", user.first_name, update.message.text)
    #cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    #db.commit()

    submit_button = [[KeyboardButton('제출하기')]]
    reply_markup = ReplyKeyboardMarkup(submit_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n혹시 내가 구한 답에 덧붙일 내용이 있으면 말해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_4_ADDED

async def question_5 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='이제 5번 문제야!',
    )

    await context.bot.send_photo(
        update.message.chat.id, open('c5.png', 'rb')
    )

    ox_button = [[KeyboardButton('맞아')], [KeyboardButton('틀렸어')]]
    reply_markup = ReplyKeyboardMarkup(ox_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 400×630야.\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 5

    return QUESTION_5

async def question_5_answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    chat_id = update.message.chat.id

    #args = (update.message.chat.id, 1, user.first_name, update.message.text)
    #logger.info("Answer of %s: %s", user.first_name, update.message.text)
    #cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    #db.commit()

    submit_button = [[KeyboardButton('제출하기')]]
    reply_markup = ReplyKeyboardMarkup(submit_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 맞았구나!\n혹시 내가 구한 답에 덧붙일 내용이 있으면 말해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_5_ADDED

async def question_5_answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    chat_id = update.message.chat.id

    #args = (update.message.chat.id, 1, user.first_name, update.message.text)
    #logger.info("Answer of %s: %s", user.first_name, update.message.text)
    #cursor.execute('INSERT INTO messages (chat_id, question_id, username, body) VALUES (%s, %s, %s, %s)', args)
    #db.commit()

    submit_button = [[KeyboardButton('제출하기')]]
    reply_markup = ReplyKeyboardMarkup(submit_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답이 틀렸구나ㅠㅠ\n혹시 내가 구한 답에 덧붙일 내용이 있으면 말해줄래?",
        reply_markup=reply_markup
    )

    return QUESTION_5_ADDED

async def end (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="오늘 준비한 수학 문제는 여기까지야!\n다음에 또 같이 공부하자ㅎㅎ 오늘 함께해줘서 고마워~"
    )

    return ConversationHandler.END

async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    if not context.user_data:
        context.user_data["question_id"] = 1

    callback_number = 3 * context.user_data["question_id"] - 2

    await context.bot.send_message(
        chat_id=chat_id, text="아래 보이는 버튼을 눌러서 알려줘!"
    )

    return callback_number

async def navigation_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    navigation_button = [[KeyboardButton('지금 문제 다시 풀기')], [KeyboardButton('다음 문제로 가기')]]
    reply_markup = ReplyKeyboardMarkup(navigation_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="고생했어! 이제 다음 문제로 넘어가도 되겠니?",
        reply_markup=reply_markup
    )

    return NAVIGATION_1

async def navigation_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    navigation_button = [[KeyboardButton('이전 문제 다시 풀기')], [KeyboardButton('이번 문제 다시 풀기')], [KeyboardButton('다음 문제로 가기')]]
    reply_markup = ReplyKeyboardMarkup(navigation_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="고생했어! 이제 다음 문제로 넘어가도 되겠니?",
        reply_markup=reply_markup
    )

    return NAVIGATION_2

async def navigation_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    navigation_button = [[KeyboardButton('이전 문제 다시 풀기')], [KeyboardButton('이번 문제 다시 풀기')], [KeyboardButton('다음 문제로 가기')]]
    reply_markup = ReplyKeyboardMarkup(navigation_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="고생했어! 이제 다음 문제로 넘어가도 되겠니?",
        reply_markup=reply_markup
    )

    return NAVIGATION_3

async def navigation_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    navigation_button = [[KeyboardButton('이전 문제 다시 풀기')], [KeyboardButton('이번 문제 다시 풀기')], [KeyboardButton('다음 문제로 가기')]]
    reply_markup = ReplyKeyboardMarkup(navigation_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="고생했어! 이제 다음 문제로 넘어가도 되겠니?",
        reply_markup=reply_markup
    )

    return NAVIGATION_4

async def navigation_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    navigation_button = [[KeyboardButton('이전 문제 다시 풀기')], [KeyboardButton('이번 문제 다시 풀기')], [KeyboardButton('학습 마무리하기')]]
    reply_markup = ReplyKeyboardMarkup(navigation_button, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="고생했어! 이제 다음 문제로 넘어가도 되겠니?",
        reply_markup=reply_markup
    )

    return NAVIGATION_5

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await context.bot.send_photo(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def callback_second(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=context.job.chat_id, photo=context.job.data)

if __name__ == '__main__':
    load_dotenv()
    application = Application.builder().token(os.environ.get('telegram-bot-token')).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [
                MessageHandler(filters.Regex("^[^준비됐어]"), warning),
                MessageHandler(filters.Regex("^\s*준비됐어\s*"), question_1)
            ],
            QUESTION_1: [
                MessageHandler(filters.Regex("^[^(맞아|틀렸어)]"), warning),
                MessageHandler(filters.Regex("^\s*맞아\s*"), question_1_answer_o),
                MessageHandler(filters.Regex("^\s*틀렸어\s*"), question_1_answer_x)
            ],
            QUESTION_1_ADDED: [
                MessageHandler(filters.Regex("^[^제출하기]"), explanation),
                MessageHandler(filters.Regex("^제출하기"), navigation_1),
            ],
            NAVIGATION_1 : [
                MessageHandler(filters.Regex("^[^(이번 문제 다시 풀기|다음 문제로 가기)]"), warning),
                MessageHandler(filters.Regex("\s*이번 문제 다시 풀기\s*"), question_1),
                MessageHandler(filters.Regex("\s*다음 문제로 가기\s*"), question_2),
            ],
            QUESTION_2: [
                MessageHandler(filters.Regex("^[^(맞아|틀렸어)]"), warning),
                MessageHandler(filters.Regex("^\s*맞아\s*"), question_2_answer_o),
                MessageHandler(filters.Regex("^\s*틀렸어\s*"), question_2_answer_x)
            ],
            QUESTION_2_ADDED: [
                MessageHandler(filters.Regex("^[^제출하기]"), explanation),
                MessageHandler(filters.Regex("^제출하기"), navigation_2),
            ],
            NAVIGATION_2: [
                MessageHandler(filters.Regex("^[^(이전 문제 다시 풀기|이번 문제 다시 풀기|다음 문제로 가기)]"), warning),
                MessageHandler(filters.Regex("\s*이전 문제 다시 풀기\s*"), question_1),
                MessageHandler(filters.Regex("\s*이번 문제 다시 풀기\s*"), question_2),
                MessageHandler(filters.Regex("\s*다음 문제로 가기\s*"), question_3),
            ],
            QUESTION_3: [
                MessageHandler(filters.Regex("^[^(맞아|틀렸어)]"), warning),
                MessageHandler(filters.Regex("^\s*맞아\s*"), question_3_answer_o),
                MessageHandler(filters.Regex("^\s*틀렸어\s*"), question_3_answer_x)
            ],
            QUESTION_3_ADDED: [
                MessageHandler(filters.Regex("^[^제출하기]"), explanation),
                MessageHandler(filters.Regex("^제출하기"), navigation_3),
            ],
            NAVIGATION_3: [
                MessageHandler(filters.Regex("^[^(이전 문제 다시 풀기|이번 문제 다시 풀기|다음 문제로 가기)]"), warning),
                MessageHandler(filters.Regex("\s*이전 문제 다시 풀기\s*"), question_2),
                MessageHandler(filters.Regex("\s*이번 문제 다시 풀기\s*"), question_3),
                MessageHandler(filters.Regex("\s*다음 문제로 가기\s*"), question_4),
            ],
            QUESTION_4: [
                MessageHandler(filters.Regex("^[^(맞아|틀렸어)]"), warning),
                MessageHandler(filters.Regex("^\s*맞아\s*"), question_4_answer_o),
                MessageHandler(filters.Regex("^\s*틀렸어\s*"), question_4_answer_x)
            ],
            QUESTION_4_ADDED: [
                MessageHandler(filters.Regex("^[^제출하기]"), explanation),
                MessageHandler(filters.Regex("^제출하기"), navigation_4),
            ],
            NAVIGATION_4: [
                MessageHandler(filters.Regex("^[^(이전 문제 다시 풀기|이번 문제 다시 풀기|다음 문제로 가기)]"), warning),
                MessageHandler(filters.Regex("\s*이전 문제 다시 풀기\s*"), question_3),
                MessageHandler(filters.Regex("\s*이번 문제 다시 풀기\s*"), question_4),
                MessageHandler(filters.Regex("\s*다음 문제로 가기\s*"), question_5),
            ],
            QUESTION_5: [
                MessageHandler(filters.Regex("^[^(맞아|틀렸어)]"), warning),
                MessageHandler(filters.Regex("^\s*맞아\s*"), question_5_answer_o),
                MessageHandler(filters.Regex("^\s*틀렸어\s*"), question_5_answer_x)
            ],
            QUESTION_5_ADDED: [
                MessageHandler(filters.Regex("^[^제출하기]"), explanation),
                MessageHandler(filters.Regex("^제출하기"), navigation_5),
            ],
            NAVIGATION_5: [
                MessageHandler(filters.Regex("^[^(이전 문제 다시 풀기|이번 문제 다시 풀기|학습 마무리하기)]"), warning),
                MessageHandler(filters.Regex("\s*이전 문제 다시 풀기\s*"), question_4),
                MessageHandler(filters.Regex("\s*이번 문제 다시 풀기\s*"), question_5),
                MessageHandler(filters.Regex("\s*학습 마무리하기\s*"), end),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
