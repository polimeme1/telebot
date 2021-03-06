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
    if (message.text.isdigit()):
        if (int(message.text) >= 1 and int(message.text) <= 10):
            answer=""
            connect = create_connection(r"./timetable.db")
            cur = connect.cursor()
            cur.execute(f"SELECT * FROM timetable WHERE groupnum == '{message.text}'")
            result = cur.fetchall()
            for i in range(len(result)):
                for j in range(2, len(result[i])-1):
                    if (j==2):
                        answer +="*" + str(result[i][j])+"*" + "\n" #Doing *bold* font-style in MarkDown
                    elif (j==3):
                        classes=str(result[i][j]).split(", ") #Split line with classes
                        place=str(result[i][j+1]).split("; ") #Split line with place
                        for k in range(len(place)):
                            classes[k] += " ("+ place[k] + ")" #Connect stings
                            answer += classes[k] + "\n"
                answer+="\n"
            bot.send_message(message.chat.id,
                             answer
                             .format(message.from_user, bot.get_me()), parse_mode='Markdown')
            connect.close()
        else:
            bot.send_message(message.chat.id,
                             "Такой группы нет!"
                             .format(message.from_user, bot.get_me()), parse_mode="html")
    else:
        bot.send_message(message.chat.id, "Пока что я не умею общаться на другие темы :( Но скоро это станет возможным!"
        .format(message.from_user, bot.get_me()), parse_mode = "html")

bot.polling(none_stop = True)