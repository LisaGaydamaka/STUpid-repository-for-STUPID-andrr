import sqlite3
import random
import telebot
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

check = 0

bot = telebot.TeleBot('1911151618:AAHG7kbTe_-s8B1Vp4HQehg6z-dcEqmnui4')

def update_db(message):
    conn = sqlite3.connect(r"C:\Users\13gai\Desktop\ffff\bott.db")
    cursor = conn.cursor()

    row = cursor.execute(
        f'SELECT count_win FROM people where id = {message.from_user.id}')
    row = row.fetchall()
    if len(row) == 0:
        insert_db(message)
    else:
        update_people(message)
    print(row)
    conn.close()


def update_people(message):
    conn = sqlite3.connect(r"C:\Users\13gai\Desktop\ffff\bott.db")
    cursor = conn.cursor()
    cursor.execute(
        f'UPDATE people SET count_win = count_win + 1 where id = {message.from_user.id}')
    conn.commit()
    conn.close()


def insert_db(message):
    conn = sqlite3.connect(r"C:\Users\13gai\Desktop\ffff\bott.db")
    cursor = conn.cursor()
    name = f'{message.chat.first_name}'
    cursor.execute(
        f'INSERT INTO people VALUES({message.from_user.id}, "{name}", 1)')
    conn.commit()
    conn.close()


def game(message):
    you = int(message.text)
    bott = random.randrange(1, 6)
    no = 'Aww too bad it was ' + str(bott)

    if bott == you:
        update_db(message)
        return 'Yep thats right'
    else:
        return no


def top_people(message):
    conn = sqlite3.connect(r"C:\Users\13gai\Desktop\ffff\bott.db")
    cursor = conn.cursor()
    row = cursor.execute(
        'SELECT name, count_win FROM people ORDER BY count_win desc')
    row = row.fetchall()
    print(row)
    count = 1
    top_string = ''
    for i in row:
        print(i[0])
        top_string += f'{count}. {i[0]}, score: {i[1]}\n'
        count += 1

    return top_string



@bot.message_handler(commands=['start'])
def start_messages(message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    markup.add(KeyboardButton('/game'), KeyboardButton('/stop'))
    markup.add(KeyboardButton('top'))
    bot.send_message(message.chat.id,
        'Type /game or press the button to start the game. Type /stop to stop. You can view the highscore board by typing "top"', reply_markup=markup)


@bot.message_handler(commands=['game'])
def get_text_messages(message):
    bot.send_message(message.chat.id, 'Alright, choose the number from 1 to 5')
    global check
    check = 1

@bot.message_handler(commands=['stop'])
def get_text_messages(message):
    bot.send_message(message.chat.id, 'Okay')
    global check
    check = 0


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if check == 1:
        if not message.text.isdigit():
            bot.send_message(message.chat.id, 'Choose the number or /stop the game')
        elif not int(message.text) in range(1, 6):
            bot.send_message(message.chat.id, 'Choose the right number')
        else:
            bot.send_message(message.chat.id, game(message))
            bot.send_message(message.chat.id, '/stop')
    else:
        if message.text.lower() == 'top':
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('Update', callback_data='update'))

            bot.send_message(message.chat.id, top_people(message))
        else:
            bot.send_message(message.chat.id, 'Huh?')


bot.polling()