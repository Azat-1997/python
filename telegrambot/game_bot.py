import telebot
from telebot import types
import random
import time
token = "Get your own token from BotFather"
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я тестовый бот, пока умею очень мало. Можете набрать /info, \
чтобы узнать перечень комманд")
    bot.send_message(message.chat.id, f"Ваш ID - {message.chat.id}")

@bot.message_handler(commands=['info'])
def get_info(message):
    bot.send_message(message.chat.id, "/info - получить перечень комманд\n\
                                       /start - приветствие от бота\n\
                                       /dice - игра в кости\n\
                                       /ssp - камень-ножницы-бумага\n")


@bot.message_handler(commands=['dice'])
def play_dice(message):
    # create keyboard object
    markup = types.InlineKeyboardMarkup()
    # and add buttons: callback_data should to be String
    markup.add(types.InlineKeyboardButton(text="Чет", callback_data="even"),
               types.InlineKeyboardButton(text="Нечет", callback_data="odd"))
    # send message
    bot.send_message(message.chat.id, text="Чет или нечет",
                     reply_markup=markup)


# SSP - Stone, Scissors, Paper
@bot.message_handler(commands=["ssp"])
def play_ssp(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Ножницы", callback_data="scissors"),
               types.InlineKeyboardButton(text="Камень", callback_data="stone"),
               types.InlineKeyboardButton(text="Бумага", callback_data="paper")
              )
    bot.send_message(message.chat.id, text="Игра в камень-ножницы бумага: твой ход.",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda dice_call: dice_call.data in ["even", "odd"])
def dice_handler(dice_call):
    bot.send_message(dice_call.message.chat.id, 'Итак...')
    time.sleep(3)
    # regular D6
    roll = random.randint(1, 6) % 2
    results = ("Чет!", "Нечет!")
    answer = results[roll]
    if dice_call.data == "even" and answer == "Чет!" or dice_call.data == "odd" and answer == "Нечет!":
       answer += ' Ты победил.'
    else:
       answer += ' Ты проиграл.'

    bot.send_message(dice_call.message.chat.id, answer)
    # Remove keyboard
    bot.edit_message_reply_markup(dice_call.message.chat.id, dice_call.message.message_id)


@bot.callback_query_handler(func=lambda ssp_call: ssp_call.data in ["scissors", "stone", "paper"])
def ssp_handler(ssp_call):
    bot.send_message(ssp_call.message.chat.id, "Ход бота...")
    time.sleep(3)
    translate = {"stone" : "камень", "scissors" : "ножницы", "paper" : "бумага"}

    bot_choice = random.choice(["stone", "scissors", "paper"]) 
    answer = ""
    win = {("stone", "scissors"), ("scissors", "paper"), ("paper", "stone")}
    if bot_choice == ssp_call.data:
       answer = f"Ничья: оба хода - {translate[ssp_call.data]}"
    elif (ssp_call.data, bot_choice) in win:
       answer = f"Вы победили: ваш ход - {translate[ssp_call.data]}, ход противника - {translate[bot_choice]}"
    else:
       answer = f"Вы проиграли: ваш ход - {translate[ssp_call.data]}, ход противника - {translate[bot_choice]}"

    bot.send_message(ssp_call.message.chat.id, answer)
    bot.edit_message_reply_markup(ssp_call.message.chat.id, ssp_call.message.message_id)


# content_types should to go after handlers with commands
@bot.message_handler(content_types='text')
def message_reply(message):
    answer_greeting = {"fuck you", "fuck you!", "fok u!", "fok u", "ебать ты!",
                       "ебать ты"}
    bot_answer = ""
    if message.text.lower() in answer_greeting:
         bot_answer = "Ответ отрицательный, Ебать ТЫ!"
    elif message.text.lower() == "oh, shit! i'm sorry.":
         bot_answer = "Sorry for what?"

    bot.send_message(message.chat.id, bot_answer)

# run "event loop"
bot.infinity_polling()





