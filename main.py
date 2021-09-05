import telebot  # импортируем библиотеку для создания бота
from telebot import types
import os
import random
import traceback
import time

bot = telebot.TeleBot('1889256380:AAFmao3mWwNTRd8aBlTn4josxH5fhr-P5Tg')  # в скобках должен быть токен


@bot.message_handler(commands=['start'])
def handle_other(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Mario', "Sonic", "Doom")
    bot.send_message(message.chat.id, """Добро пожаловать!
Что бы узнать все команды введите /help
А пока предлагаю узнать больше о с самых популярных играх этого года👇""", reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, """/start - начало программы
/help - подсказка по всем командам
/sound_m - католог соундреков к марио
/art - случайный игровой арт
""")

@bot.message_handler(commands=['art'])
def handle_art(message):
    all_file = os.listdir('files/img/other')
    img = open('files/img/other/' + random.choice(all_file), 'rb')  # соединяем путь к файлу и его имя, открываем для чтения и в двоичном режиме
    bot.send_chat_action(message.chat.id, 'upload_photo')  # сообщить пользователю о загрузке фото
    bot.send_photo(message.chat.id, img)  # отправить фото в чат
    img.close()  # закрыть файл

@bot.message_handler(commands=['sound_m'])
def handle_sound(message):
    all_file = os.listdir('files/audio/Mario')
    for i in range(3):
        audio = open('files/audio/Mario/' + all_file[i], 'rb')
        bot.send_chat_action(message.chat.id, 'upload_audio')
        bot.send_audio(message.chat.id, audio)
        audio.close()
    bot.send_message(message.chat.id, "Наслаждайся🐸")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Mario':
        directory = 'files/img/Mario'
        all_file = os.listdir(directory)
        img = open(directory + '/' + all_file[0], 'rb') # соединяем путь к файлу и его имя, открываем для чтения и в двоичном режиме
        bot.send_chat_action(message.chat.id, 'upload_photo') # сообщить пользователю о загрузке фото
        bot.send_photo(message.chat.id, img) # отправить фото в чат
        img.close() # закрыть файл
        bot.send_message(message.chat.id, 'Приключения Марио, энергичного героя Грибного королевства!\nА какая музыка😁')
        audio = open('files/audio/Mario/smb-overworld.mp3', 'rb')
        bot.send_chat_action(message.chat.id, 'upload_audio')
        bot.send_audio(message.chat.id, audio)
        audio.close()
    elif message.text == 'Sonic':
        directory = 'files/img/Sonic'
        img = open(directory + '/' + '1.jpg', 'rb') # соединяем путь к файлу и его имя, открываем для чтения и в двоичном режиме
        bot.send_chat_action(message.chat.id, 'upload_photo') # сообщить пользователю о загрузке фото
        bot.send_photo(message.chat.id, img) # отправить фото в чат
        img.close() # закрыть файл
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_d = types.InlineKeyboardButton(text='Добро', callback_data='s_d')  # кнопка «Да»
        key_z = types.InlineKeyboardButton(text='Зло', callback_data='s_z')
        key_n = types.InlineKeyboardButton(text='Нейтрал', callback_data='s_n')
        keyboard.row(key_d, key_z, key_n)
        bot.send_message(message.chat.id, text='Тест: Кто ты из Соника?🦊\n На какой ты стороне?', reply_markup=keyboard)
    elif message.text == 'Doom':
        bot.send_message(message.chat.id, 'Самые популярная игра текущего года')
        bot.send_message(message.chat.id, 'Но тут пока ничего нет')

@bot.callback_query_handler(func=lambda call: call.data.startswith('s'))
def callback_worker_reg(call):
    print('1')
    directory = 'files/img/Sonic'
    img = ''
    if call.data == "s_d":
        bot.send_message(call.message.chat.id, 'Вы получили: Ёж Соник')
        img = open(directory + '/' + 'sonic.png', 'rb')
    elif call.data == "s_z":
        bot.send_message(call.message.chat.id, 'Вы получили: Доктор Эггман')
        img = open(directory + '/' + 'tsr_doctor_eggman.png', 'rb')
    elif call.data == "s_n":
        bot.send_message(call.message.chat.id, 'Вы получили: Ёж Шэдоу')
        img = open(directory + '/' + 'yozh-shedou.png', 'rb')
    bot.send_chat_action(call.message.chat.id, 'upload_photo')
    bot.send_photo(call.message.chat.id, img)
    img.close()


def write_log(text_log):
    file_log = open('log.txt', 'a')
    file_log.write('\n' + str(text_log))
    file_log.close()

while True:
    try:
        print('Bot running..') #
        bot.polling(none_stop=True, interval=2) # запуск бота
    except Exception: # ловим ошибку
        erro_text = traceback.format_exc()
        print(erro_text) # выводим весь текст ошибки в консоль
        write_log(erro_text)
        print('Restarting..')
        bot.stop_polling() # останавливаем работу бота
        time.sleep(10) # делаем паузу перед запуском
