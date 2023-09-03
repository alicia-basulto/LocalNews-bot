import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import *
from dotenv import load_dotenv
from telebot import types
#from logger import startLogger
import os
import telebot


load_dotenv()
#Telegram Bot API token
api_secret = os.getenv("API_SECRET")
API_TOKEN = api_secret

# URL of the webpage to extract data from
URL = "https://www.lavozdemedinadigital.com/wordpress/category/medina-del-campo/"
print(API_TOKEN)
bot = telebot.TeleBot(API_TOKEN)
#logger = startLogger()
# Create an Updater instance
#updater = Updater(API_TOKEN)
#dispatcher = updater.dispatcher


commands = {  # command description used in the "help" command
    'start': 'Start the bot',
}

if __name__ == '__main__':
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        chat_id = message.chat.id
        bot.send_message(chat_id,
                         "<b>Welcome to LocalNewsBot</b>\nIn this chatbot you will get updated by the recent news published in your favourite local newspaper",
                         parse_mode="HTML")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        bot.reply_to(message, 'What would you like to do?', reply_markup=markup)
    bot.polling()



# Function to send a message to the Telegram chat
def send_message(update, context, text):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=text)

# Function to scrape and send new notices
def send_new_notices(context: CallbackContext):
    # Get the content HTML of the webpage
    response = requests.get(URL)
    content = response.content

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Find the list of notices
    notice_list = soup.findAll('div', class_='td-module-thumb')

    # Iterate through the notices and send them as messages
    for element in notice_list:
        block = element.find('a')
        notice_title = block['title']
        chat_id = context.job.context
        send_message(context, chat_id, text=notice_title)

print('Starting a bot....')
