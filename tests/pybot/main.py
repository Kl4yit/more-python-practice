#!/usr/bin/env python
# -*- coding: utf-8 -*-



import logging
import os
import time
from isIsomorphic import is_isomorphic

import flask

import telebot

API_TOKEN = '<token>'

WEBHOOK_HOST = 'webhook-py-bot.herokuapp.com'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr


WEBHOOK_URL_BASE = "https://%s" % (WEBHOOK_HOST)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return '!', 200


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
    return '!', 200



INTRO = '''
Привет!

/speak - чтобы поговорить

/isomorphic - проверить изоморфность матриц
'''
MAT_TYPE = '''
Введите матрицу вида:

1 2 3 4
5 6 7 8
4 3 2 9
'''


@bot.message_handler(commands=['speak', 'isomorphic'])
def start1(message):
    global INTRO
    global MAT_TYPE
    if message.text == '/speak':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, PollUser().get_name) #следующий шаг – функция get_name
    elif message.text == '/isomorphic':
        bot.send_message(message.from_user.id, MAT_TYPE)
        bot.register_next_step_handler(message, Isom().get_matrix)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /help')


@bot.message_handler(commands=['help'])
def start1(message):
    global INTRO
    global MAT_TYPE
    if message.text == '/help':
        bot.send_message(message.from_user.id, INTRO)



@bot.message_handler(content_types=['text'])
def start2(message):
    bot.send_message(message.from_user.id, 'Напиши /help')


class Isom:
    def __init__(self):
        self.A = None
        self.B = None

    def get_matrix(self, message):
        self.A = self.parse_string(message)
        self._swap()
        if not self.A:
            bot.send_message(message.from_user.id, MAT_TYPE)
            bot.register_next_step_handler(message, self.get_matrix)
        else:
            self.calc_isom(message)

    def parse_string(self, message):
        a = message.text
        try:
            arr = [list(map(int, a)) for a in [i.split() for i in a.strip().split('\n')]]
        except BaseException:
            bot.send_message(message.from_user.id, 'Плохая матрица!')
            bot.register_next_step_handler(message, self.get_matrix)
            return
        return arr

    def _swap(self):
        self.A, self.B = self.B, self.A

    def calc_isom(self, message):
        res = is_isomorphic(self.A, self.B)
        if res:
            bot.send_message(message.from_user.id, 'Матрицы изоморфны')
            return
        bot.send_message(message.from_user.id, 'Матрицы не изоморфны')


class PollUser:

    def __init__(self):
        self.data = {}

    def get_name(self, message): #получаем фамилию

        self.data['name'] = message.text
        bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
        bot.register_next_step_handler(message, self.get_surname)

    def get_surname(self, message):
        self.data['surname'] = message.text
        bot.send_message(message.from_user.id, 'Сколько тебе лет?')
        bot.register_next_step_handler(message, self.get_age)



    def get_age(self, message):

        try:
            self.data['age'] = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
            bot.register_next_step_handler(message, self.get_age)
            return
        keyboard = telebot.types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = f"Тебе {str(self.data['age'])} лет, тебя зовут {self.data['name']} {self.data['surname']}?"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Попробуйте снова /speak')





time.sleep(1)
# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

time.sleep(1)
# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

# Start flask server
if __name__ == '__main__':
    app.run(host=WEBHOOK_LISTEN,
            port=int(os.environ.get('PORT', WEBHOOK_PORT))
            )
