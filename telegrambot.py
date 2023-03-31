import telebot
from telebot import types
from bs4 import BeautifulSoup as bs
import requests
from multiprocessing import Pool
import ast
import json


token = '6085985269:AAE9Ff9_7iUN0u9mOapNIItMAMG7eACDB6k'
bot = telebot.TeleBot(token)

keyboard_start = types.ReplyKeyboardMarkup()

button_userlist = types.KeyboardButton('Users list')
button_posts = types.KeyboardButton('Posts list')
button_overall = types.KeyboardButton('Overall statistics')

keyboard_start.add(button_userlist)
keyboard_start.add(button_posts)
keyboard_start.add(button_overall)


def parse_users():
    soup = bs(requests.get('http://localhost:8000/parsing/userlist_info/').text, 'lxml')
    text = soup.find('p').text
    ordered_dict = json.loads(text)
    returning_list = []
    for item in ordered_dict:
        returning_list.append(f'First name: {item["first_name"]}\nLast name: {item["last_name"]}\nUser name: {item["username"]}\n\
Email: {item["email"]}\nID: {item["id"]}\nAdmin: {item["is_superuser"]}')
    return returning_list


def parse_posts():
    soup = bs(requests.get('http://localhost:8000/parsing/postlist_info/').text, 'lxml')
    text = soup.find('p').text
    ordered_dict = json.loads(text)
    returning_list = []
    for item in ordered_dict:
        returning_list.append(f'Post ID: {item["id"]}\nTitle: {item["title"]}\nAuthor: {item["owner_username"]}\n\
Comments: {item["comments"]}')
    return returning_list


def parse_overall():
    soup = bs(requests.get('http://localhost:8000/parsing/overall_stats/').text,'lxml')
    text = soup.find('p').text
    ordered_dict = json.loads(text)
    return ordered_dict


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello this is Hackathon Unify project \
                     parser')
    answer = bot.send_message(message.chat.id, 'Choose what you want?', reply_markup=keyboard_start)
    bot.register_next_step_handler(answer, handle_answer)


@bot.message_handler(commands=['stop'])
def stop_message(message):
    bot.send_message(message.chat.id, 'Goodbye!')


def handle_answer(message):
    if message.text.lower() == 'users list':
        users_list(message)
    elif message.text.lower() == 'posts list':
        posts_list(message)
    elif message.text.lower() == 'overall statistics':
        overall_stats(message)
    else:
        answer = bot.send_message(message.chat.id, 'what?', reply_markup=keyboard_start)
        bot.register_next_step_handler(answer, handle_answer)


def users_list(message):
    result = parse_users()
    for item in result:
        bot.send_message(message.chat.id, item)
    answer = bot.send_message(message.chat.id, 'Choose what you want?', reply_markup=keyboard_start)
    bot.register_next_step_handler(message, handle_answer)


def posts_list(message):
    result = parse_posts()
    for item in result:
        bot.send_message(message.chat.id, item)
    answer = bot.send_message(message.chat.id, 'Choose what you want?', reply_markup=keyboard_start)
    bot.register_next_step_handler(message, handle_answer)


def overall_stats(message):
    result = parse_overall()
    msg = f'Posts count: {result["posts_count"]}\nUsers count: {result["users_count"]}\n\
How much messages sent: {result["messages_count"]}\n\nRequest handled at\n{result["request_date"]}'
    bot.send_message(message.chat.id, msg)
    answer = bot.send_message(message.chat.id, 'Choose what you want?', reply_markup=keyboard_start)
    bot.register_next_step_handler(message, handle_answer)


bot.polling()
