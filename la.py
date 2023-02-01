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
    MessageHandler,
    CallbackQueryHandler,
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
START, QUESTION_1, QUESTION_1_ADDED, QUESTION_2, QUESTION_2_ADDED, QUESTION_3, QUESTION_3_ADDED, QUESTION_4, QUESTION_4_ADDED, QUESTION_5, QUESTION_5_ADDED, \
QUESTION_6, QUESTION_6_ADDED, QUESTION_7, QUESTION_7_ADDED, QUESTION_8, QUESTION_8_ADDED, QUESTION_9, QUESTION_9_ADDED, QUESTION_10, QUESTION_10_ADDED, \
QUESTION_11, QUESTION_11_ADDED, QUESTION_12, QUESTION_12_ADDED, QUESTION_13, QUESTION_13_ADDED, QUESTION_14, QUESTION_14_ADDED, QUESTION_15, QUESTION_15_ADDED, \
QUESTION_16, QUESTION_16_ADDED, QUESTION_17, QUESTION_17_ADDED, QUESTION_18, QUESTION_18_ADDED, QUESTION_19, QUESTION_19_ADDED, QUESTION_20, QUESTION_20_ADDED, \
QUESTION_21, QUESTION_21_ADDED, QUESTION_22, QUESTION_22_ADDED, QUESTION_23, QUESTION_23_ADDED, QUESTION_24, QUESTION_24_ADDED, QUESTION_25, QUESTION_25_ADDED, \
QUESTION_26, QUESTION_26_ADDED, QUESTION_27, QUESTION_27_ADDED, QUESTION_28, QUESTION_28_ADDED, QUESTION_29, QUESTION_29_ADDED, QUESTION_30, QUESTION_30_ADDED, \
QUESTION_31, QUESTION_31_ADDED, QUESTION_32, QUESTION_32_ADDED, QUESTION_33, QUESTION_33_ADDED, QUESTION_34, QUESTION_34_ADDED, QUESTION_35, QUESTION_35_ADDED = range(71)

mode = "la"

async def jump_to (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    chat_id = update.message.chat.id

    number_button = [[InlineKeyboardButton('1', callback_data='1'), InlineKeyboardButton('2', callback_data='2'), InlineKeyboardButton('3', callback_data='3'),  InlineKeyboardButton('4', callback_data='4'), InlineKeyboardButton('5', callback_data='5')],
                     [InlineKeyboardButton('6', callback_data='6'), InlineKeyboardButton('7', callback_data='7'), InlineKeyboardButton('8', callback_data='8'),  InlineKeyboardButton('9', callback_data='9'), InlineKeyboardButton('10', callback_data='a')],
                     [InlineKeyboardButton('11', callback_data='b'), InlineKeyboardButton('12', callback_data='c'), InlineKeyboardButton('13', callback_data='d'), InlineKeyboardButton('14', callback_data='e'), InlineKeyboardButton('15', callback_data='f')],
                     [InlineKeyboardButton('16', callback_data='g'), InlineKeyboardButton('17', callback_data='h'), InlineKeyboardButton('18', callback_data='i'), InlineKeyboardButton('19', callback_data='j'), InlineKeyboardButton('20', callback_data='k')],
                     [InlineKeyboardButton('21', callback_data='l'), InlineKeyboardButton('22', callback_data='m'), InlineKeyboardButton('23', callback_data='n'), InlineKeyboardButton('24', callback_data='o'), InlineKeyboardButton('25', callback_data='p')],
                     [InlineKeyboardButton('26', callback_data='q'), InlineKeyboardButton('27', callback_data='r'), InlineKeyboardButton('28', callback_data='s'), InlineKeyboardButton('29', callback_data='t'), InlineKeyboardButton('30', callback_data='u')],
                     [InlineKeyboardButton('31', callback_data='v'), InlineKeyboardButton('32', callback_data='w'), InlineKeyboardButton('33', callback_data='x'), InlineKeyboardButton('34', callback_data='y'), InlineKeyboardButton('35', callback_data='z')],
                     ]

    reply_markup = InlineKeyboardMarkup(number_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="시작할 문제 번호를 클릭해주세요",
        reply_markup=reply_markup
    )

    context.user_data["question_id"] = 0

    return 119

async def start (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="안녕 반가워😊\n\n나는 오늘 너와 함께 도형 문제를 풀 챗봇이야~~ \n\n오늘 우리는 20분 동안 수학의 도형 부분을 공부하게 될 거야!"
    )

    await context.bot.send_message(
        chat_id=chat_id, text="내가 푼 문제들이 맞았는지 틀렸는지에 대해 조언을 부탁해!\n\n난 너의 조언에 귀 기울일 준비가 되어있어👂"
    )

    start_button = [[InlineKeyboardButton('준비됐어', callback_data='준비됐어')]]

    reply_markup = InlineKeyboardMarkup(start_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text='너도 준비가 되었다면, 아래 보이는 <준비됐어> 버튼을 클릭해줘!\n\n오늘 잘 부탁해!',
        reply_markup=reply_markup
    )

    return START

async def question_1 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그럼 1번 문제부터 풀어볼게!',
    )

    await context.bot.send_photo(
        chat_id, open('a1.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 식은\n\n16×14÷2야!\n\n내가 구한 식이 맞니?🤔",
        reply_markup= reply_markup
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
        text='알려줘서 정말 고마워~!\n\n다음은 2번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a2.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 생각엔 90×60인 것 같은데,\n\n내가 구한 식이 맞니?",
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
        text='아하 그렇구나!!\n\n고마워~ 다음은 3번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a3.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 식은\n\n(200+60)×140÷2야~\n\n내가 구한 식이 맞았는지 알려줄 수 있어?",
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
        text='나도 열심히 이해해볼게💪\n\n다음은 4번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a4.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 15×8이라고 생각해!!\n\n어때? 내 식이 맞을까?🧐",
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
        text='너와 함께 문제를 풀 수 있어서 행복해😘\n\n다음은 5번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a5.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은\n\n400×630÷2인데,\n\n내가 맞게 풀었을까??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 5

    return QUESTION_5

async def question_6 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='설명 고마워!\n\n다음은 6번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a6.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 식은 4×8야!!\n\n내가 식을 맞게 구한걸까?🙏🏻",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 6

    return QUESTION_6

async def question_7 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음에도 멋진 설명 부탁해😆 \n\n다음은 7번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a7.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 구해봤는데 \n\n35×35가 나왔어!!\n\n내가 구한 게 맞니~?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 7

    return QUESTION_7

async def question_8 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 고마워!\n\n다음은 8번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a8.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 18×25÷2이야!\n\n내 식이 맞다고 생각해, 아님 틀리다고 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 8

    return QUESTION_8

async def question_9 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음 문제들도 열심히 풀어볼게🙌🏻 \n\n다음은 9번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a9.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 25×50÷2라고 생각해ㅎㅎ\n\n내 식이 맞을까??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 9

    return QUESTION_9

async def question_10 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='친절하게 알려줘서 고마워!\n\n다음은 10번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a10.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은\n\n7×9÷2야!\n\n내가 구한 게 맞았을까?🤔",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 10

    return QUESTION_10

async def question_11 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='아하 그렇게 생각했구나~!!! \n\n다음은 11번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a11.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은\n\n105×68인데,\n\n어떻게 생각해?🤩",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 11

    return QUESTION_11

async def question_12 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='너가 도와줘서 문제 푸는게 재밌어😙\n\n다음은 12번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a12.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 구해보니, (12+8)×2가 나왔어!!\n\n내가 구한 게 맞을까??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 12

    return QUESTION_12

async def question_13 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='아하 그렇구나!\n\n다음은 13번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a13.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은\n\n15×7÷2야~\n\n내가 잘 구한 걸까?🧐",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 13

    return QUESTION_13

async def question_14 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='날 도와줘서 정말 고마워~ \n\n다음은 14번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a14.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 7×12÷2라고 생각해!!\n\n너는 내 식이 맞았다고 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 14

    return QUESTION_14

async def question_15 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='아하! 다음 문제도 잘 부탁해!\n\n다음은 15번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a15.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은\n\n30×80÷2야.\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 15

    return QUESTION_15

async def question_16 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='나도 그렇게 생각해! 다음은 16번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a16.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 식은\n\n(5+15)×6이야!\n\n내 식에 대해 어떻게 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 16

    return QUESTION_16

async def question_17 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='너의 설명 꼭 기억할게💪🏻\n\n다음은 17번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a17.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 구해봤는데, 4×6÷2가 나왔어~\n\n내가 구한 게 맞니?🙏",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 17

    return QUESTION_17

async def question_18 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 고마워! 다음은 18번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a18.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은\n\n20+9+9야!\n\n내가 구한 식을 어떻게 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 18

    return QUESTION_18

async def question_19 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='너의 설명이 정말 도움이 되고 있어!\n\n다음 19번 문제도 잘 부탁해~',
    )

    await context.bot.send_photo(
        chat_id, open('a19.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 열심히 식을 구해봤는데\n\n(24+4)×15가 나왔어!\n\n내가 맞게 푼걸까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 19

    return QUESTION_19

async def question_20 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='너랑 같이 공부하니 정말 재밌어!\n\n다음은 20번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a20.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 3×4÷2야~!\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 20

    return QUESTION_20

async def question_21 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 알려줘서 고마워~ 다음은 21번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a21.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 식은 7×4인데,\n\n너가 생각하기엔 어때~??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 21

    return QUESTION_12

async def question_22 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='너의 설명 덕분에 힘이 난다! 다음은 22번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a22.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 식을 구해봤는데 말이야~\n\n30×18가 나왔어!\n\n내가 구한 게 맞을까😙?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 22

    return QUESTION_22

async def question_23 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나 그렇구나! 다음은 23번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a23.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 4×20야!\n\n내가 구한 식이 맞다고 생각해?😆",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 23

    return QUESTION_23

async def question_24 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 고마워! 다음 문제도 잘 부탁해🤩\n\n이제 24번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a24.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 9×8라고 생각하는데 어때?\n\n내 식이 맞을까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 24

    return QUESTION_24

async def question_25 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 고마워! 다음은 25번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a25.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은\n\n9×12÷2인데,\n\n내가 구한 결과가 어떻다고 생각해?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 25

    return QUESTION_25

async def question_26 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나~ 너랑 같이 공부할 수 있어서 행복해🤗 다음 26번 문제도 잘 부탁해!',
    )

    await context.bot.send_photo(
        chat_id, open('a26.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 25x16÷2야!\n\n내가 구한 게 맞았니?🧐",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 26

    return QUESTION_26

async def question_27 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='자세한 설명 고마워!\n\n다음 문제는 27번이야~',
    )

    await context.bot.send_photo(
        chat_id, open('a27.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 구해봤는데, 24x10÷2가 나왔어!!\n\n내가 구한 게 맞다고 생각하니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 27

    return QUESTION_27

async def question_28 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='나도 너와 같은 생각이야!! 다음 28번 문제도 잘 부탁해~',
    )

    await context.bot.send_photo(
        chat_id, open('a28.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각해봤는데, 식은 150×90÷2인 것 같아!\n\n내가 구한 식이 맞다고 생각해?🤔",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 28

    return QUESTION_28

async def question_29 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나!\n\n너의 설명 꼭 기억할게💪🏻 다음은 29번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a29.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 (6+12)×2라고 생각하는데 어때?\n\n내 식이 맞을까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 29

    return QUESTION_29

async def question_30 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='잘 알려줘서 고마워! 다음은 30번이야~',
    )

    await context.bot.send_photo(
        chat_id, open('a30.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은\n\n6×4야!!\n\n내가 잘 풀었다고 생각해~?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 30

    return QUESTION_30

async def question_31 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='너가 도와줘서 문제 푸는 게 재밌어😙\n\n다음은 31번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a31.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 구해보니, 11×11이 나왔어!!\n\n내가 구한 게 맞을까??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 31

    return QUESTION_31

async def question_32 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='아하 그렇구나! 다음은 32번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a32.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은\n\n15×12÷2야~\n\n내가 잘 풀은걸까?🧐",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 32

    return QUESTION_32

async def question_33 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='아 그렇네! 날 도와줘서 정말 고마워~ 다음은 33번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a33.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 25×15÷2라고 생각해!!\n\n너는 내 식이 맞았다고 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 33

    return QUESTION_33

async def question_34 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='아하! 다음 문제도 잘 부탁해!\n\n다음은 34번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('a34.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 18×10÷2야.\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 34

    return QUESTION_34

async def question_35 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 정말 고마워~! 이제 35번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('a35.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 식은\n\n(5+10)×6÷2야!\n\n너는 내 식에 대해 어떻게 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 35

    return QUESTION_35

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
            [InlineKeyboardButton('밑변은 16, 높이는 14이기 때문에 식을 세워보면, 16×14÷2야', callback_data='1')],
            [InlineKeyboardButton('밑변은 16, 높이는 16라서 식을 세워보면, 16×16÷2야', callback_data='2')],
            [InlineKeyboardButton('밑변은 16, 높이는 14이기 때문에 식을 세워보면, 16×14야', callback_data='3')],
            [InlineKeyboardButton('밑변은 14, 높이는 16이기 때문에 식을 세워보면, 14×16가 돼', callback_data='4')]
        ],
        2 : [
            [InlineKeyboardButton('한 대각선이 90, 다른 대각선이 60이기 때문에 90×60이야', callback_data='1')],
            [InlineKeyboardButton('한 대각선이 90, 다른 대각선은 60이므로 90×60÷2야', callback_data='2')],
            [InlineKeyboardButton('한 대각선이 90, 다른 대각선은 30이기 때문에 90×30÷2야', callback_data='3')],
            [InlineKeyboardButton('한 대각선이 45, 다른 대각선은 길이가 60이므로 45×60÷2야', callback_data='4')]
        ],
        3 : [
            [InlineKeyboardButton('윗변은 140, 아랫변은 200, 높이가 60이니까 (140+200)×60÷2야', callback_data='1')],
            [InlineKeyboardButton('윗변은 200, 아랫변은 60, 높이는 140이니까 (200+60)×140÷2야', callback_data='2')],
            [InlineKeyboardButton('윗변은 140, 아랫변이 60, 높이가 200이니까 (140+60)×200÷2야', callback_data='3')],
            [InlineKeyboardButton('윗변은 60, 아랫변이 140, 높이는 200이니까 (60+140)×200이야', callback_data='4')]
        ],
        4 : [
            [InlineKeyboardButton('세로는 8니까 식은 8×8이야', callback_data='1')],
            [InlineKeyboardButton('가로는 15니까 식은 15×15야', callback_data='2')],
            [InlineKeyboardButton('가로는 15, 세로는 8이니까 식을 세워보면 (15+8)×2야', callback_data='3')],
            [InlineKeyboardButton('가로는 15 이고 세로는 8이니까 식을 구해보면 15×8이야', callback_data='4')]
        ],
        5 : [
            [InlineKeyboardButton('밑변은 400이고 높이는 630이기 때문에 식은 400×630이야', callback_data='1')],
            [InlineKeyboardButton('밑변은 400이고 높이는 630이기 때문에 식이 400×630÷2야', callback_data='2')],
            [InlineKeyboardButton('밑변은 200이고 높이는 630이기 때문에 식이 200×630이야', callback_data='3')],
            [InlineKeyboardButton('밑변은 630이고 높이는 400이라서 식은 630×400이야', callback_data='4')]
        ],
        6 : [
            [InlineKeyboardButton('한 변의 길이가 4이고 변이 4개니까 식을 세워보면 4×4야', callback_data='1')],
            [InlineKeyboardButton('한 변의 길이가 4이고 변은 6개니까 식은 4×6이 맞아', callback_data='2')],
            [InlineKeyboardButton('한 변이 4이고 변이 8개여서 식은 4×8이 돼', callback_data='3')],
            [InlineKeyboardButton('한 변의 길이가 6이고 변이 4개라서 식은 6×4야', callback_data='4')]
        ],
        7 : [
            [InlineKeyboardButton('한 변이 35이기 때문에 식을 구해보면 35×4가 돼', callback_data='1')],
            [InlineKeyboardButton('한 변이 30이기 때문에 식을 구해보면 30×30이 돼', callback_data='2')],
            [InlineKeyboardButton('한 변이 35이고, 정사각형의 넓이는 35×35를 하면 돼', callback_data='3')],
            [InlineKeyboardButton('한 변이 35이기 때문에 식을 구해보면 35×35÷2가 돼', callback_data='4')]
        ],
        8 : [
            [InlineKeyboardButton('밑변은 18이고 높이는 18이니까 18×18÷2가 맞아', callback_data='1')],
            [InlineKeyboardButton('밑변은 25이고 높이는 18이라서 식은 25×18이야', callback_data='2')],
            [InlineKeyboardButton('밑변은 18이고 높이는 25이기 때문에 식은 18×25÷2가 돼', callback_data='3')],
            [InlineKeyboardButton('밑변은 18이고 높이는 18이니까 18×18이 맞는 식이야', callback_data='4')]
        ],
        9 : [
            [InlineKeyboardButton('한 대각선이 40, 다른 대각선은 50이라서 식은 40×50이야', callback_data='1')],
            [InlineKeyboardButton('한 대각선이 40, 다른 대각선은 50이니까 식이 40×50÷2야', callback_data='2')],
            [InlineKeyboardButton('한 대각선이 25, 다른 대각선은 50이니까 식은 25×50÷2야', callback_data='3')],
            [InlineKeyboardButton('한 대각선이 40, 다른 대각선은 50이니까 식이 20×50÷2야', callback_data='4')]
        ],
        10 : [
            [InlineKeyboardButton('밑변은 7이고 높이는 9니까 식은 7×9÷2야', callback_data='1')],
            [InlineKeyboardButton('밑변은 7이고 높이는 9니까 식은 7×9×2가 맞아', callback_data='2')],
            [InlineKeyboardButton('밑변은 9이고 높이는 7니까 식은 9×7÷2라고 세우면 돼', callback_data='3')],
            [InlineKeyboardButton('밑변은 9이고 높이는 7이기 때문에 식은 9×7이 나와', callback_data='4')]
        ],
        11 : [
            [InlineKeyboardButton('가로는 105이고 세로는 68이니까 식은 105+68이야', callback_data='1')],
            [InlineKeyboardButton('가로는 105이고 세로는 68이기 때문에 식이 105×68이 나와', callback_data='2')],
            [InlineKeyboardButton('가로는 105이고 세로는 68이라서 식은 (105+68)×2가 맞아', callback_data='3')],
            [InlineKeyboardButton('가로는 105이고 세로는 60이니까 식은 105×60라고 세우면 돼', callback_data='4')]
        ],
        12 : [
            [InlineKeyboardButton('한 변이 12이고 다른 변은 10이니까 식은 12+10이야', callback_data='1')],
            [InlineKeyboardButton('한 변이 12이고 다른 변이 10이니까 식은 (12+10)×2야', callback_data='2')],
            [InlineKeyboardButton('한 변이 12이고 다른 변은 8이니까 (12+8)×2가 맞아', callback_data='3')],
            [InlineKeyboardButton('한 변이 12이고 다른 변이 8이라서 12×8이야', callback_data='4')]
        ],
        13 : [
            [InlineKeyboardButton('윗변은 15이고 아랫변이 9, 높이는 7니까 (15+9)×7÷2가 맞아', callback_data='1')],
            [InlineKeyboardButton('윗변은 15이고 높이는 7이니까 식을 구하면 15×7÷2가 나와', callback_data='2')],
            [InlineKeyboardButton('윗변은 15이고 아랫변은 9, 높이는 9니까 식은 (15+9)×9÷2야', callback_data='3')],
            [InlineKeyboardButton('윗변은 15이고 아랫변은 9, 높이는 7니까 식은 (15+9)×7이야', callback_data='4')]
        ],
        14 : [
            [InlineKeyboardButton('밑변은 12이고 높이는 7이니까 식은 12×7÷2가 맞아', callback_data='1')],
            [InlineKeyboardButton('밑변은 7이고 높이는 12니까 식을 구해보면 7×12가 나와', callback_data='2')],
            [InlineKeyboardButton('밑변은 7이고 높이는 12니까 식은 7×12÷2야', callback_data='3')],
            [InlineKeyboardButton('밑변은 12이고 높이는 7이니까 식은 12×7이야', callback_data='4')]
        ],
        15 : [
            [InlineKeyboardButton('밑변은 30이고 높이는 80이니까 30×80이 맞아', callback_data='1')],
            [InlineKeyboardButton('밑변은 30이고 높이는 80이기 때문에 식은 30×80÷2가 맞아', callback_data='2')],
            [InlineKeyboardButton('밑변은 80이고 높이는 30이니까 식은 80×30라고 세우면 돼', callback_data='3')],
            [InlineKeyboardButton('밑변은 80이고 높이는 30이라서 식은 80×30÷2야', callback_data='4')]
        ],
        16 : [
            [InlineKeyboardButton('윗변은 5, 아랫변은 15, 높이가 6이니까 식은 (5+15)×6이야', callback_data='1')],
            [InlineKeyboardButton('윗변은 5, 아랫변이 15, 높이는 6이니까 (5+15)×6÷2야', callback_data='2')],
            [InlineKeyboardButton('아랫변은 15이고 높이는 6이기 때문에 식이 15×6÷2가 돼', callback_data='3')],
            [InlineKeyboardButton('윗변은 5, 아랫변이 15, 높이는 6이니까 (5+15)×6이 맞아', callback_data='4')]
        ],
        17 : [
            [InlineKeyboardButton('한 대각선이 4이고 다른 대각선은 6이니까 4×6이 맞아', callback_data='1')],
            [InlineKeyboardButton('한 대각선이 6, 다른 대각선은 4이기 때문에 식은 (4+6)×2야', callback_data='2')],
            [InlineKeyboardButton('한 대각선이 6, 다른 대각선은 6이니까 6×6÷2야', callback_data='3')],
            [InlineKeyboardButton('한 대각선이 4, 다른 대각선은 6이니까 4×6÷2가 돼', callback_data='4')]
        ],
        18 : [
            [InlineKeyboardButton('가로는 20이고 세로는 9니까 20+9+9가 돼', callback_data='1')],
            [InlineKeyboardButton('가로는 20니까 식을 구해보면 20+20이 돼', callback_data='2')],
            [InlineKeyboardButton('세로가 9니까 식을 세워보면 9×4가 돼', callback_data='3')],
            [InlineKeyboardButton('가로는 20이고 세로는 9니까 (20+9)×2가 돼', callback_data='4')]
        ],
        19 : [
            [InlineKeyboardButton('윗변은 24, 아랫변이 4, 높이는 15니까 (24+4)×15÷2가 돼', callback_data='1')],
            [InlineKeyboardButton('윗변은 24, 아랫변이 15, 높이는 4니까 (24+15)×4÷2가 나와', callback_data='2')],
            [InlineKeyboardButton('윗변은 24, 아랫변이 4, 높이는 15니까 (24+4)×15가 돼', callback_data='3')],
            [InlineKeyboardButton('높이는 15, 아랫변이 4니까 식은 15×4÷2가 돼', callback_data='4')]
        ],
        20: [
            [InlineKeyboardButton('밑변은 3이고 높이는 4이기 때문에 식이 3×4야', callback_data='1')],
            [InlineKeyboardButton('밑변은 3이고 높이는 4이니까 식은 3×4÷2야', callback_data='2')],
            [InlineKeyboardButton('밑변은 4이고 높이는 3이기 때문에 식은 (4+3)×2야', callback_data='3')],
            [InlineKeyboardButton('밑변은 3이고 높이는 5이므로 식은 3×5야', callback_data='4')]
        ],
        21 : [
            [InlineKeyboardButton('세로는 4니까 식은 4×4야', callback_data='1')],
            [InlineKeyboardButton('가로는 7, 세로는 4니까 식을 세워보면 (7+4)×2야', callback_data='2')],
            [InlineKeyboardButton('가로는 7이고 세로는 4니까 식을 구해보면 7×4야', callback_data='3')],
            [InlineKeyboardButton('가로는 7니까 식은 7×7이야', callback_data='4')]
        ],
        22 : [
            [InlineKeyboardButton('한 대각선이 30, 다른 대각선은 18이어서 식은 30×18이 돼', callback_data='1')],
            [InlineKeyboardButton('한 대각선이 15, 다른 대각선은 18이므로 15×18이야', callback_data='2')],
            [InlineKeyboardButton('한 대각선이 30, 다른 대각선은 18이라 식은 30×18÷2야', callback_data='3')],
            [InlineKeyboardButton('한 대각선이 30, 다른 대각선은 9니까 30×9÷2가 돼', callback_data='4')]
        ],
        23 : [
            [InlineKeyboardButton('밑변은 4이고, 높이는 20이니까 식이 4×20이 돼', callback_data='1')],
            [InlineKeyboardButton('밑변은 4이고, 높이는 20이어서 식은 4×20÷2가 돼', callback_data='2')],
            [InlineKeyboardButton('밑변은 20이고, 높이는 4이므로 식이 20×4가 돼', callback_data='3')],
            [InlineKeyboardButton('밑변은 16이고, 높이는 20이어서 식은 16×20÷2가 돼', callback_data='4')]
        ],
        24 : [
            [InlineKeyboardButton('한 변이 9, 변의 수는 7개니까 식을 구해보면 9×7가 돼', callback_data='1')],
            [InlineKeyboardButton('한 변이 9, 변의 수는 6개니까 9×6이 돼', callback_data='2')],
            [InlineKeyboardButton('한 변이 18, 변의 수는 7개니까 식은 18×7이야', callback_data='3')],
            [InlineKeyboardButton('한 변이 9, 변의 수가 8개니까 식을 세워보면 9×8이야', callback_data='4')]
        ],
        25 : [
            [InlineKeyboardButton('윗변은 9, 아랫변이 14, 높이는 12니까 (9+14)×12÷2가 돼', callback_data='1')],
            [InlineKeyboardButton('윗변은 12, 아랫변은 14, 높이는 9니까 (12+14)×9÷2가 나와', callback_data='2')],
            [InlineKeyboardButton('윗변은 9, 높이는 12니까 식은 9×12÷2가 돼', callback_data='3')],
            [InlineKeyboardButton('높이는 12, 아랫변이 14니까 식이 12×14÷2가 돼', callback_data='4')]
        ],
        26 : [
            [InlineKeyboardButton('밑변은 25, 높이는 16이기 때문에 식이 25×16이 돼', callback_data='1')],
            [InlineKeyboardButton('밑변은 25, 높이는 16이기 때문에 식이 25×16÷2가 돼', callback_data='2')],
            [InlineKeyboardButton('밑변은 16, 높이는 25이기 때문에 식은 16×25÷2야', callback_data='3')],
            [InlineKeyboardButton('밑변은 50, 높이는 16이기 때문에 식은 50×16이야', callback_data='4')]
        ],
        27 : [
            [InlineKeyboardButton('한 대각선이 10, 다른 대각선은 24이므로 식은 10×24야', callback_data='1')],
            [InlineKeyboardButton('한 대각선이 10, 다른 대각선은 13이어서 10×13이야', callback_data='2')],
            [InlineKeyboardButton('한 대각선이 10, 다른 대각선은 13이니까 10×13÷2이야', callback_data='3')],
            [InlineKeyboardButton('한 대각선이 24, 다른 대각선은 10이기 때문에 24×10÷2야', callback_data='4')]
        ],
        28 : [
            [InlineKeyboardButton('밑변은 150, 높이는 90이기 때문에 식은 150×90÷2가 돼', callback_data='1')],
            [InlineKeyboardButton('밑변은 150, 높이는 90이기 때문에 식이 150×90이 돼', callback_data='2')],
            [InlineKeyboardButton('밑변은 180, 높이는 150이니까 식은 180×150÷2가 돼', callback_data='3')],
            [InlineKeyboardButton('밑변은 180, 높이는 90이니까 식을 만들면 180×90÷2가 돼', callback_data='4')]
        ],
        29 : [
            [InlineKeyboardButton('가로는 6이니까 식은 6×6이야', callback_data='1')],
            [InlineKeyboardButton('세로는 12니까 식은 12×12야', callback_data='2')],
            [InlineKeyboardButton('가로는 6, 세로는 12니까 식을 세워보면 (6+12)×2야', callback_data='3')],
            [InlineKeyboardButton('가로는 6이고 세로는 12니까 식을 구해보면 6×12야', callback_data='4')]
        ],
        30 : [
            [InlineKeyboardButton('한 변이 6이고 변의 개수가 4개니까 6×4가 돼', callback_data='1')],
            [InlineKeyboardButton('한 변은 6이고 변의 개수는 3개니까 테두리의 길이는 6×3이 돼', callback_data='2')],
            [InlineKeyboardButton('한 변이 6이고 변은 3개니까 테두리 길이가 6×3÷2야', callback_data='3')],
            [InlineKeyboardButton('한 변이 3이고 변은 3개니까 테두리 길이는 3×3이야', callback_data='4')]
        ],
        31 : [
            [InlineKeyboardButton('한 변이 11이기 때문에 식을 구해보면 11×11이 돼', callback_data='1')],
            [InlineKeyboardButton('한 변이 22이기 때문에 식을 세워보면 22×22가 돼', callback_data='2')],
            [InlineKeyboardButton('한 변이 11이고, 정사각형의 넓이는 11×4를 하면 돼', callback_data='3')],
            [InlineKeyboardButton('한 변이 11이기 때문에 식을 구해보면 11×11÷2가 돼', callback_data='4')]
        ],
        32 : [
            [InlineKeyboardButton('밑변은 15이고 높이는 12이기 때문에 식이 15×12÷2야', callback_data='1')],
            [InlineKeyboardButton('밑변은 15이고 높이는 5이기 때문에 식은 15×5야', callback_data='2')],
            [InlineKeyboardButton('밑변은 5이고 높이는 12이기 때문에 식을 세우면 5×12야', callback_data='3')],
            [InlineKeyboardButton('밑변은 5이고 높이는 15라서 식이 5×15야', callback_data='4')]
        ],
        33 : [
            [InlineKeyboardButton('밑변은 20, 높이는 15이므로 식을 구하면 20×15÷2가 돼', callback_data='1')],
            [InlineKeyboardButton('밑변은 25, 높이는 15라서 식은 25×15÷2가 돼', callback_data='2')],
            [InlineKeyboardButton('밑변은 20, 높이는 15여서 식을 세우면 20×15가 되네', callback_data='3')],
            [InlineKeyboardButton('밑변은 15, 높이는 25이므로 식은 15×25÷2가 나와', callback_data='4')]
        ],
        34 : [
            [InlineKeyboardButton('한 대각선이 18, 다른 대각선은 10이어서 식은 18×10이야', callback_data='1')],
            [InlineKeyboardButton('한 대각선이 18, 다른 대각선은 5이므로 18×5÷2야', callback_data='2')],
            [InlineKeyboardButton('한 대각선이 9, 다른 대각선은 10이니까 9×10÷2가 나와', callback_data='3')],
            [InlineKeyboardButton('한 대각선이 18, 다른 대각선은 10이니까 18×10÷2야', callback_data='4')]
        ],
        35: [
            [InlineKeyboardButton('윗변이 6, 아랫변은 10, 높이는 5이니까 (6+10)×5÷2가 돼', callback_data='1')],
            [InlineKeyboardButton('윗변이 5, 아랫변이 10, 높이는 6이니까 식은 (5+10)×6÷2가 나와', callback_data='2')],
            [InlineKeyboardButton('윗변은 5, 아랫변은 10, 높이는 6이니까 식이 (5+10)×6가 돼', callback_data='3')],
            [InlineKeyboardButton('윗변은 6, 아랫변은 10, 높이는 5니까 (6+10)×5가 돼', callback_data='4')]
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
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, mode, question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_identifier) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

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
    application = Application.builder().token(os.environ.get('la_math_bot')).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [
                CallbackQueryHandler(question_1, pattern="^\s*준비됐어\s*"),
                MessageHandler(filters.Regex("\s*번호\s*입력\s*"), jump_to),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            119 : [
                CallbackQueryHandler(question_1, pattern="1"),
                CallbackQueryHandler(question_2, pattern="2"),
                CallbackQueryHandler(question_3, pattern="3"),
                CallbackQueryHandler(question_4, pattern="4"),
                CallbackQueryHandler(question_5, pattern="5"),
                CallbackQueryHandler(question_6, pattern="6"),
                CallbackQueryHandler(question_7, pattern="7"),
                CallbackQueryHandler(question_8, pattern="8"),
                CallbackQueryHandler(question_9, pattern="9"),
                CallbackQueryHandler(question_10, pattern="a"),
                CallbackQueryHandler(question_11, pattern="b"),
                CallbackQueryHandler(question_12, pattern="c"),
                CallbackQueryHandler(question_13, pattern="d"),
                CallbackQueryHandler(question_14, pattern="e"),
                CallbackQueryHandler(question_15, pattern="f"),
                CallbackQueryHandler(question_16, pattern="g"),
                CallbackQueryHandler(question_17, pattern="h"),
                CallbackQueryHandler(question_18, pattern="i"),
                CallbackQueryHandler(question_19, pattern="j"),
                CallbackQueryHandler(question_20, pattern="k"),
                CallbackQueryHandler(question_21, pattern="l"),
                CallbackQueryHandler(question_22, pattern="m"),
                CallbackQueryHandler(question_23, pattern="n"),
                CallbackQueryHandler(question_24, pattern="o"),
                CallbackQueryHandler(question_25, pattern="p"),
                CallbackQueryHandler(question_26, pattern="q"),
                CallbackQueryHandler(question_27, pattern="r"),
                CallbackQueryHandler(question_28, pattern="s"),
                CallbackQueryHandler(question_29, pattern="t"),
                CallbackQueryHandler(question_30, pattern="u"),
                CallbackQueryHandler(question_31, pattern="v"),
                CallbackQueryHandler(question_32, pattern="w"),
                CallbackQueryHandler(question_33, pattern="x"),
                CallbackQueryHandler(question_34, pattern="y"),
                CallbackQueryHandler(question_35, pattern="z")
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
                CallbackQueryHandler(question_6, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_6: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_6_ADDED: [
                CallbackQueryHandler(question_7, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_7: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_7_ADDED: [
                CallbackQueryHandler(question_8, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_8: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_8_ADDED: [
                CallbackQueryHandler(question_9, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_9: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_9_ADDED: [
                CallbackQueryHandler(question_10, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_10: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_10_ADDED: [
                CallbackQueryHandler(question_11, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_11: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_11_ADDED: [
                CallbackQueryHandler(question_12, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_12: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_12_ADDED: [
                CallbackQueryHandler(question_13, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_13: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_13_ADDED: [
                CallbackQueryHandler(question_14, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_14: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_14_ADDED: [
                CallbackQueryHandler(question_15, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_15: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_15_ADDED: [
                CallbackQueryHandler(question_16, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_16: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_16_ADDED: [
                CallbackQueryHandler(question_17, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_17: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_17_ADDED: [
                CallbackQueryHandler(question_18, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_18: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_18_ADDED: [
                CallbackQueryHandler(question_19, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_19: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_19_ADDED: [
                CallbackQueryHandler(question_20, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_20: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_20_ADDED: [
                CallbackQueryHandler(question_21, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_21: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_21_ADDED: [
                CallbackQueryHandler(question_22, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_22: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_22_ADDED: [
                CallbackQueryHandler(question_23, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_23: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_23_ADDED: [
                CallbackQueryHandler(question_24, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_24: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_24_ADDED: [
                CallbackQueryHandler(question_25, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_25: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_25_ADDED: [
                CallbackQueryHandler(question_26, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_26: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_26_ADDED: [
                CallbackQueryHandler(question_27, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_27: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_27_ADDED: [
                CallbackQueryHandler(question_28, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_28: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_28_ADDED: [
                CallbackQueryHandler(question_29, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_29: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_29_ADDED: [
                CallbackQueryHandler(question_30, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_30: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_30_ADDED: [
                CallbackQueryHandler(question_31, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_31: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_31_ADDED: [
                CallbackQueryHandler(question_32, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_32: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_32_ADDED: [
                CallbackQueryHandler(question_33, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_33: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_33_ADDED: [
                CallbackQueryHandler(question_34, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_34: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_34_ADDED: [
                CallbackQueryHandler(question_35, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_35: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_35_ADDED: [
                CallbackQueryHandler(end, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
