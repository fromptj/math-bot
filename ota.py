import logging
import pymysql
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
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# Connect database with chatbot and move on to chatbot database
db = pymysql.connect(host="localhost", user="root", charset="utf8mb4")
cursor = db.cursor()
cursor.execute('USE chatbot;')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# QUESTION 1 : 1 / QUESTION 2 : 3 / QUESTION 3 : 5 / QUESTION 4 : 7 / QUESTION 5 : 9
# QUESTION_1_ADDED : 2 / QUESTION_2_ADDED : 4 / QUESTION_3_ADDED : 6 / QUESTION_4_ADDED : 8 / QUESTION_5_ADDED : 10
START, QUESTION_1, QUESTION_1_ADDED, QUESTION_2, QUESTION_2_ADDED, QUESTION_3, QUESTION_3_ADDED, QUESTION_4, QUESTION_4_ADDED, QUESTION_5, QUESTION_5_ADDED = range(11)

mode = "ota"

async def explanation (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    chat_id = update.message.chat.id

    args = (chat_id, mode, context.user_data["question_id"], user.id, update.message.text)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, cond, question_id, user_id, explanation) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    return 2 * context.user_data["question_id"]

async def start (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="안녕 반가워😊 나는 오늘 너와 함께 공부할 연습용 챗봇이야.\n내가 문제 5개를 풀었는데, 내 답이 맞았는지 틀렸는지에 대해 조언을 부탁할게!"
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

    # update.callback_query.edit_message_reply_markup(None)
    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그럼 1번 문제부터 풀어볼게!',
    )

    await context.bot.send_photo(
        chat_id, open('ot1.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 답은 18900÷21이야.\n\n내가 구한 답이 맞니?🤔",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 1

    return QUESTION_1



async def question_2 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 고마워! 다음은 2번 문제야~',
    )

    await context.bot.send_photo(
       chat_id, open('ot2.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="답을 구해보니, (15+20+10+15)÷4이 나왔어.\n\n내가 구한 게 정답이니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 2

    return QUESTION_2

async def question_3 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='아하 그렇게 생각했구나~!!! 다음은 3번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('ot3.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 답은 (43+45+35+40+33+51+40)÷6이야.\n\n내가 구한 답이 맞았는지 알려줄 수 있어?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 3

    return QUESTION_3

async def question_4 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='너가 도와줘서 문제 푸는게 재밌어😙 다음은 4번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('ot4.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 답이 (5+4+2+1)÷4라고 생각해!!\n\n어때? 내 답이 맞을까?🧐",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 4

    return QUESTION_4

async def question_5 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 고마워! 다음은 5번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('ot5.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 480+6이야.\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 5

    return QUESTION_5

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    answer_o_text = [
        "내 식이 맞다니 다행이야😉\n\n그럼 식을 구하는 과정은 어떻게 되니?",
        "와 맞았다!!😆\n\n식을 구하는 과정을 설명해줄래?",
        "내가 제대로 풀었구나😉\n\n식을 구하는 과정은 어떻게 되는지 설명해줄 수 있어?",
        "내가 맞았구나!🤩\n\n식을 구하는 과정을 설명해줄 수 있니?"
    ]

    answer_x_text = [
        "내 식이 틀렸구나ㅠㅠ\n\n그럼 식을 구하는 과정을 설명해줄래?",
        "앗 내가 틀렸구나😭\n\n그럼 식을 구하는 과정은 어떻게 되니?",
        "내 식이 틀렸구나ㅠ🥲\n\n그럼 식을 구하는 과정을 설명해줄래?",
        "내가 틀리게 풀었구나ㅠ_ㅠ\n\n그럼 식을 구하는 법을 설명해줄 수 있니?"
    ]

    submit_button = {
        1 : [
            [InlineKeyboardButton('3주일은 20일이니까 18900÷20을 하면 돼', callback_data='1')],
            [InlineKeyboardButton('1주일이 7일이고 3주일은 21일이니까 18900÷21을 하면 돼', callback_data='2')],
            [InlineKeyboardButton('1주일이 6일이고 3주일은 18일이니까 18900÷18을 하면 돼', callback_data='3')],
            [InlineKeyboardButton('3주일은 14일이니까 18900÷20을 하면 돼', callback_data='4')],
        ],
        2 : [
            [InlineKeyboardButton('전체 딱지 수가 15+20+10이고, 학생은 4명이어서 (15+20+10)×4야', callback_data='1')],
            [InlineKeyboardButton('전체 딱지는 15+20+10+15개고, 학생은 4명이니까 (15+20+10+15)÷4야', callback_data='2')],
            [InlineKeyboardButton('전체 딱지는 15+20+10+15개고, 학생은 3명이니까 (15+20+10+15)÷3이야', callback_data='3')],
            [InlineKeyboardButton('전체 딱지 수가 15+20+10이고, 학생은 3명이어서 (15+20+10)×3이야', callback_data='4')],
        ],
        3 : [
            [InlineKeyboardButton('월~일까지의 43+45+35+40+33+51+40개의 달걀을 7로 나누면 돼', callback_data='1')],
            [InlineKeyboardButton('월~일까지의 43+45+35+40+33+51+40개의 달걀을 6으로 나누면 돼', callback_data='2')],
            [InlineKeyboardButton('월~일까지의 43+45+35+40+33+51개의 달걀을 6으로 나누면 돼', callback_data='3')],
            [InlineKeyboardButton('월~일까지의 43+45+35+40+33+51개의 달걀을 7으로 나누면 돼', callback_data='4')],
        ],
        4 : [
            [InlineKeyboardButton('1,2,3,4일에 읽은 책의 총합인 5+4+2+1을 3로 나누어주면 돼', callback_data='1')],
            [InlineKeyboardButton('1,2,3,4일에 읽은 책의 총합인 5+2+1을 4로 나누어주면 돼', callback_data='2')],
            [InlineKeyboardButton('1,2,3,4일에 읽은 책의 총합인 5+4+2+1을 4로 나누어주면 돼', callback_data='3')],
            [InlineKeyboardButton('1,2,3,4일에 읽은 책의 총합인 5+4+1을 4로 나누어주면 돼', callback_data='4')],
        ],
        5 : [
            [InlineKeyboardButton('왕복 전체 거리 960km를 전체 걸린 시간인 6시간으로 나누면 돼', callback_data='1')],
            [InlineKeyboardButton('전체 거리 480km를 왕복 걸린 시간인 12시간으로 나누면 돼', callback_data='2')],
            [InlineKeyboardButton('왕복 전체 거리 960km를 왕복 걸린 시간인 12시간으로 나누면 돼', callback_data='3')],
            [InlineKeyboardButton('전체 거리 480km를 전체 걸린 시간인 6시간으로 나누면 돼', callback_data='4')],
        ]
    }

    reply_markup = InlineKeyboardMarkup(submit_button[question_id])

    await context.bot.send_message(
        chat_id=chat_id,
        text= answer_o_text[question_id % 4] if update.callback_query.data == "맞아" else answer_x_text[question_id % 4], # % 뒤의 숫자는 answer_text의 개수만큼으로 한다
        reply_markup=reply_markup
    )

    return 2 * question_id


async def end (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="준비한 수학 문제는 여기까지야!\n다음에 또 같이 공부하자ㅎㅎ 함께해줘서 고마워~"
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
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await context.bot.send_photo(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

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
    application = Application.builder().token(os.environ.get('ota_math_bot')).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [
                CallbackQueryHandler(question_1, pattern="^\s*준비됐어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_1: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_1_ADDED: [
                CallbackQueryHandler(question_2, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_2: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_2_ADDED: [
                CallbackQueryHandler(question_3, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_3: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_3_ADDED: [
                CallbackQueryHandler(question_4, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_4: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_4_ADDED: [
                CallbackQueryHandler(question_5, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_5: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_5_ADDED: [
                CallbackQueryHandler(end, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
