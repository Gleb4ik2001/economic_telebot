import telebot
from decouple import config
from database_connection.database import Database
from database_connection.tasks_db import Tasks

conn : Database = Database(
    host=config('HOST',cast = str),
    port=config('PORT',cast = int),
    user=config('USER',cast = str),
    password=config('PASSWORD',cast = str),
    db_name= config('DB_NAME',cast = str)
)


TOKEN = config('TOKEN',cast=str)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message:dict):
    text = f'Привет,<b> {message.chat.first_name}</b>. Отправь мне номер билета и я скину решение'
    markup = telebot.types.InlineKeyboardMarkup()
    btn_start = telebot.types.InlineKeyboardButton(
        'Начать',
        callback_data='btn_start'
    )
    btn_exit = telebot.types.InlineKeyboardButton(
        'Выйти',
        callback_data='btn_exit'
    )
    markup.add(btn_start,btn_exit)
    bot.send_message(
        message.chat.id,
        text=text,parse_mode='HTML',
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call:dict):
    if call.data =='btn_start':
        bot.send_message(
            call.message.chat.id,
            'Отправьте номер билета'
        )
    elif call.data == 'btn_exit':
        bot.send_message(
            call.message.chat.id,
            'Выход'
        )
    
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )

@bot.message_handler(func=lambda message: message.text.isdigit())
def send_bilet_data(message):
    try:
        text = Tasks.find_bilet(
            conn=conn.conn,
            bilet_number=int(message.text)
        )
        if not text:
            bot.send_message(
                message.chat.id,
                'Такого билета нет в БД'
            )
        else:
            bot.send_message(
                message.chat.id,
                text=text
            )
    except Exception as exc:
        bot.send_message(
            message.chat.id,
            text=exc
        )


if __name__ =='__main__':
    bot.polling(non_stop=True)
