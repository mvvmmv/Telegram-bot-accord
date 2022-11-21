import telebot
from datetime import datetime
import logging

import functions

BOT_API = ''
bot = telebot.TeleBot(BOT_API)

# глобальные перменные для хранения введенных пользователем значений
input_key = ''
input_lad = ''

# настройки для логирования
logging.basicConfig(
    level=logging.ERROR,
    filename="errorlog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: \
              %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)

# еще один вид логирования


def logging_decorator(func):
    '''Декоратор логирования'''
    def wrapper(message):
        with open('log.txt', 'a') as f:
            f.write(str(message.text)+'  ' +
                    str(datetime.fromtimestamp(message.date))+'  ' +
                    str(message.from_user.id)+'  ' +
                    str(message.from_user.is_bot)+'  ' +
                    str(message.from_user.first_name)+'  ' +
                    str(message.from_user.last_name)+'  ' +
                    str(message.from_user.username)+'  ' +
                    str(message.from_user.language_code)+'\n')
        func(message)
    return wrapper


@bot.message_handler(commands=['start'])
@logging_decorator
def start(message):
    '''Обработчик команды /start'''

    bot.send_message(message.chat.id, 'Привет, '+str(message.chat.first_name) +
                     '. Чтобы узнать что может бот введи команду /help')


@bot.message_handler(commands=['help'])
@logging_decorator
def help(message):
    '''Обработчик команды /help'''

    bot.send_message(message.chat.id,
                     "Список возможных запросов:\n<b>Лады</b>, <b>лад</b> - покажет все лады, имеющиеся в программе\n<b>Тональность</b>, <b>тон</b>, <b>ноты</b>, <b>нота</b> - покажет все ноты\n<b>Гамма</b> - покажет гамму в заданном ладу от заданной ноты\n<b>Аккорды</b>, <b>аккорд</b> - покажет основные аккорды в заданной тональности", parse_mode='html')


@bot.message_handler(content_types=['text'])
@logging_decorator
def get_user_text(message):
    '''Обработчик текста, вводимого пользователем'''

    input_text = (message.text).lower()
    if input_text in ['лады', 'лад']:
        bot.send_message(message.chat.id, ', '.join(
            list(functions.get_harmonies().keys())))
    elif input_text in ['тональность', 'тон', 'ноты', 'нота']:
        bot.send_message(message.chat.id, '  '.join(functions.get_gamma()))

    elif input_text in ['гамма']:
        # спросить тон, лад (по умолчанию натуральный мажор)
        # рисуется клавиатура со всеми ключами из get_gamma
        key = draw_buttons(functions.get_gamma())
        msg = bot.send_message(
            message.chat.id, 'В каком ключе?', reply_markup=key)
        bot.register_next_step_handler(msg, get_key, input_text)

    elif input_text in ['аккорды', 'аккорд']:
        # спросить тон, лад (по умолчанию натуральный мажор)
        key = draw_buttons(functions.get_gamma())
        msg = bot.send_message(
            message.chat.id, 'В каком ключе?', reply_markup=key)
        bot.register_next_step_handler(msg, get_key, input_text)
    else:
        msg = bot.send_message(
            message.chat.id, 'Не понял. Попробуйте другой запрос.\nНапример, "гамма". "лад", "тональность", "аккорды"')


def get_key(message, init_request):
    '''Сохраняет ответ пользователя(нота) и задает следующий вопрос(какой
    лад)'''

    global input_key
    input_key = message.text

    if input_key not in functions.get_gamma():
        bot.send_message(message.chat.id, 'Введенное значение некорректно')
    else:
        harmony = draw_buttons(list(functions.get_harmonies().keys()))
        msg = bot.send_message(
            message.chat.id, 'Какой лад?', reply_markup=harmony)
        bot.register_next_step_handler(msg, get_harm, init_request)


def get_harm(message, init_request):
    '''Сохраняет ответ пользователя(лад) и отправляет в ответ
    аккорды или гамму в зависимости от запроса init_request и предыдущего
    ответа'''

    global input_lad
    input_lad = message.text

    if input_lad not in list(functions.get_harmonies().keys()):
        bot.send_message(message.chat.id, 'Введенное значение некорректно')
    else:
        if init_request in ['гамма']:
            gamma = functions.get_gamma_by_key_and_harmony(
                input_key, input_lad)
            bot.send_message(message.chat.id, '  '.join(gamma))
        elif init_request in ['аккорды', 'аккорд']:
            chords = functions.get_chords_by_key_and_harmony(
                input_key, input_lad)
            bot.send_message(message.chat.id, '  '.join(chords))


def draw_buttons(list: list):
    '''Рисует клавиатуру для ответов пользователя'''

    markup = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True, row_width=3)
    for text in list:
        button = telebot.types.KeyboardButton(text)
        markup.add(button)
    return markup


bot.polling(non_stop=True)
