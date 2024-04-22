import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('7087185963:AAGiaylZIHla-cxKcIl595prBDS-STzds3I')

admin = '1380312622'
mail = ''
from_goods = False


@bot.message_handler(commands=['start'])
def main(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сделать заказ")
    btn2 = types.KeyboardButton("Связаться со службой поддержки")
    btn3 = types.KeyboardButton("Наш сайт")
    markup1.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     f"Доброго времени суток! Пожалуйста, выберите что вам необходимо".format(
                         message.from_user), reply_markup=markup1)


@bot.message_handler(content_types=['text'])
def callback_message(message):
    try:
        global from_goods
        if message.text == "Наш сайт":
            bot.send_message(message.chat.id,
                             f"Вот ссылка на наш сайт: {'///'}")
        elif message.text == "Сделать заказ":
            if not mail:
                bot.send_message(message.from_user.id, f'Пожалуйста, напишите свою почту:')
                from_goods = True
                bot.register_next_step_handler(message, linked_mail)
                return from_goods
            else:
                bot.send_message(message.from_user.id,
                                 f'Прикрепите ссылку на товар который хотите приобрести:')
                bot.register_next_step_handler(message, linked_goods)

        elif message.text == 'Связаться со службой поддержки':
            if not mail:
                bot.send_message(message.from_user.id, f'Пожалуйста, напишите свою почту:')
                bot.register_next_step_handler(message, linked_mail)
            else:
                bot.send_message(message.from_user.id,
                                 f'Напишите свое обращение, и мы вам обязательно ответим в ближайшее время:')
                bot.register_next_step_handler(message, takes_from_users)

        elif message.text == "Получить промокод":
            pass
    except Exception as ex:
        bot.reply_to(message, ex)


def linked_goods(message):
    try:
        global mail, from_goods

        user = message.from_user.id
        promt = message.text
        user_name = message.from_user.full_name
        mail_to_db = mail
        with sqlite3.connect('db/users_of_tg.db') as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (user, promt, user_name, mail) VALUES (?, ?, ?, ?);",
                           (user, promt, user_name, mail_to_db))
            cursor.close()
        bot.send_message(message.from_user.id,
                         f'Спасибо! Мы обязательно ответим вам в ближайшее время')
        bot.send_message('1380312622', message.text)
        from_goods = False
    except Exception as ex:
        bot.reply_to(message, ex)


def takes_from_users(message):
    try:
        global mail, from_goods
        promt = message.text
        mail_to_db = mail
        with sqlite3.connect('db/users_of_tg.db') as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO takes (mail, take) VALUES (?, ?);",
                           (mail_to_db, promt))
            cursor.close()
        bot.send_message(message.from_user.id,
                         f'Спасибо! Мы обязательно ответим вам в ближайшее время')
        bot.send_message('1380312622', message.text)
        from_goods = False
    except Exception as ex:
        bot.reply_to(message, ex)


def linked_mail(message):
    try:
        global from_goods
        if from_goods:
            global mail
            mail = message.text
            bot.send_message(message.from_user.id,
                             f'Прикрепите ссылку на товар который хотите приобрести:')
            bot.register_next_step_handler(message, linked_goods)
            return mail
        else:
            mail = message.text
            bot.send_message(message.from_user.id,
                             f'Напишите свое обращение, и мы вам обязательно ответим в ближайшее время:')
            bot.register_next_step_handler(message, takes_from_users)
            return mail

    except Exception as ex:
        bot.reply_to(message, ex)


bot.polling(none_stop=True)
