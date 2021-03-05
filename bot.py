import telebot
import config
from database import *

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row("1", "2", "3", "4")
    bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот-расписание для потока Бизнес-информатики."
                     .format(message.from_user, bot.get_me()), parse_mode = "html", reply_markup=keyboard)

@bot.message_handler(commands=["help"])
def helpme(message):
    bot.send_message(message.chat.id, "Я - бот, который показывает расписание для всего потока на каждый день.\n"
                                      "Для того, чтобы посмотреть расписание, нажми на последнюю цифру номера группы."
                     .format(message.from_user, bot.get_me()), parse_mode = "html")

@bot.message_handler(content_types = ["text"])
def mytext(message):
    if (int(message.text) >= 1 and int(message.text) <= 10):
        connect = create_connection(r"D:\projects\bot\timetable.db")
        cur = connect.cursor()
        cur.execute(f"SELECT * FROM timetable WHERE groupnum == '{message.text}'")  # вывести день, пары и аудитории
        result = cur.fetchall()
        # parse your string and check what button was pressed
        # create var with request from DB
        bot.send_message(message.chat.id,result, parse_mode="html")
        # bot.send_message(message.chat.id, *your request from DB*
        # .format(message.from_user, bot.get_me()), parse_mode = "html")
        connect.close()
    else:
        bot.send_message(message.chat.id, "Пока что я не умею общаться на другие темы :( Но скоро это станет возможным!"
        .format(message.from_user, bot.get_me()), parse_mode = "html")

bot.polling(none_stop = True)