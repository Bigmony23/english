import random

import telebot

from logger import Logger
from urllib.request import urlopen
from settings import config
from data import *




log = Logger(config.BOT_NAME[1:])  # Without '@'
bot = telebot.TeleBot(config.BOT_TOKEN, parse_mode="html")
log.info(f"Bot <{config.BOT_NAME}> started")


@bot.message_handler(commands=["start"])
def answer_start(message):
    bot.send_photo(message.chat.id, START_IMAGE_URL, text_commands["start"])
    log.info(f"START user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")


@bot.message_handler(commands=["commands"])
def answer_commands(message):
    bot.send_message(message.chat.id, text_commands["commands"])
    log.info(f"COMMANDS user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")


@bot.message_handler(commands=["about"])
def answer_about(message):
    bot.send_message(message.chat.id, text_commands["about"])
    log.info(f"ABOUT user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")


@bot.message_handler(commands=["englishwords"])
def answer_english_words(message):
    nouns = "\n".join([f"🔻 {noun}" for noun in words["nouns"]])
    verbs = "\n".join([f"🔻 {verb}" for verb in words["verbs"]])

    bot.send_photo(message.chat.id, "https://disk.yandex.ru/i/7WG0dU2SrJkdnA",
                   text_commands["english_words"].format(nouns, verbs))
    log.info(f"ENGLISH WORDS user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")

# @bot.message_handler(commands=['file'])
# def send_welcome(message):
#     doc = urlopen('https://docs.google.com/spreadsheets/d/1bA0UKbGt-kyeXSi3Bd1a1BrQPgJ-l681/edit?usp=sharing&ouid=107664573538241031180&rtpof=true&sd=true\most_used_english_words.xlsx')
#     bot.send_doc(message.chat.id, file)
    # doc = open(' 'rb')
    # bot.send_document(message.from_user.id, doc)
    # doc.close()
@bot.message_handler(commands=["questions"])
def answer_questions(message):
    global word
    word = random.choice(words_list)
    bot.send_message(message.chat.id, text=f'Напиши перевод слова "{word}" на русский язык')
    bot.register_next_step_handler(message,check_answer)
def check_answer(message):
    for words_en in bukva_A1:
        if words_en ==word:
            words_ru=bukva_A1[words_en]
            if message.text.lower()==words_ru:
                bot.send_message(message.chat.id,text=f'Верно {words_en} равно {words_ru}\n  Продолжим /questions\n')
                break

            else:
                bot.send_message(message.chat.id,text=f'Неверно {words_en} равно {words_ru}\n Продолжим /questions\n')
                break





    # translated_messages = ""
    # for partes_of_spech in bukva_A1:
    #     for bukva_ru in words_ru:
    #         if message.text.lower()==bukva_ru:
    #             translated_messages=f' Верно {words_en} равно на {words_ru}'
    #             bot.send_message(message.chat.id, translated_messages)
    #             log.info(
    #                 f"TRANSLATED user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>, "
    #                                          f"text=<{message.text}>")
    #             break
    # if not translated_messages:
    #
    #
    #
    #     bot.send_message(message.chat.id, text=f'Неверно {words_en} равно на {words_ru}'.format(message.chat.first_name))
    #     log.info(f"RECV user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>, "
    #              f"text=<{message.text}>")
    #




# def check_answer(message):
#
#     translated_message = ""
#     print(message)
#     for part_of_speech in bukva_A1:
#         for word in bukva_A1[part_of_speech]:
#             if message.text.lower() == word:
#                 translated_message = f"{dictionary[part_of_speech].title()}: {message.text.lower()}\n" \
#                                      f"Перевод: {bukva_A1[part_of_speech][word]}\n\n" \
#                                      f"Отправьте /englishwords, чтобы посмотреть список слов"
#                 bot.send_message(message.chat.id, translated_message)
#                 log.info(f"User_Answer user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>, "
#                          f"text=<{message.text}>")
#                 break
#     if not translated_message:
#         bot.send_message(message.chat.id, text_commands["default"].format(message.chat.first_name))
#         log.info(f"RECV user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>, "
#                  f"text=<{message.text}>")


@bot.message_handler(func=lambda x: True)
def answer_to_all_messages(message):
    translated_message = ""
    for part_of_speech in words:
        for word in words[part_of_speech]:
            if message.text.lower() == word:
                translated_message = f"{dictionary[part_of_speech].title()}: {message.text.lower()}\n" \
                                     f"Перевод: {words[part_of_speech][word]}\n\n" \
                                     f"Отправьте /englishwords, чтобы посмотреть список слов"
                bot.send_message(message.chat.id, translated_message)
                log.info(f"TRANSLATED user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>, "
                         f"text=<{message.text}>")
                break
    if not translated_message:
        bot.send_message(message.chat.id, text_commands["default"].format(message.chat.first_name))
        log.info(f"RECV user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>, "
                 f"text=<{message.text}>")

bot.polling(none_stop=True)
log.warning(f"Bot <{config.BOT_NAME}> finished")
