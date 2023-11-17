# Import required libraries
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import *
from dotenv import load_dotenv
from telebot import types
from logger import startLogger
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import googleapiclient.discovery
# Load environment variables
load_dotenv()
# Retrieve YouTube API token from environment variables
api_youtube = os.getenv("API_YOUTUBE")

# Create YouTube API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_youtube)

# Retrieve channel ID from channel username
channel_username = "TelemedinaCanal9"

# Check if channel was found
channels_response = youtube.channels().list(
    part="id",
    forUsername=channel_username
).execute()

# Verifica si se encontró un canal
if channels_response.get("items"):
    channel_id = channels_response["items"][0]["id"]

    # Luego, obtén la lista de vídeos del canal por su ID
    videos = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=10,
        order="date" # Puedes ajustar el número de resultados aquí
    ).execute()

    # Itera a través de los resultados e imprime los títulos y URL de los vídeos
    for video in videos["items"]:
        video_title = video["snippet"]["title"]
        

else:
    print("No se encontró un canal con el nombre de usuario proporcionado.")


# Retrieve Telegram Bot API token from environment variables
api_secret = os.getenv("API_SECRET")
API_TOKEN = api_secret

# URL of the webpage to extract data from
URL = "https://www.lavozdemedinadigital.com/wordpress/category/medina-del-campo/"
bot = telebot.TeleBot(API_TOKEN)
logger = startLogger()

# Define commands for the bot
commands = {  # command description used in the "help" command
    'start': 'Start the bot',
    'help': 'Request help'
}


#TODO user introduces link from youtube and news web customized
#TODO user introduces the number of news to see
#TODO bot saves the user status
#TODO bot sends notifications every time upcoming news are uploaded in the web
if __name__ == '__main__':
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        chat_id = message.chat.id
        bot.send_message(chat_id,
                         "<b>Welcome to LocalNewsBot</b>\nIn this chatbot you will get updated by the recent news published in your favourite local newspaper",
                         parse_mode="HTML")
        markup = create_buttons()
        bot.send_message(message.chat.id, "Hi! What are the news that you want to see?", reply_markup=markup)
    # Define function to create reply keyboard with buttons
    def create_buttons():
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("Youtube")
        item2 = types.KeyboardButton("Newspaper")
        markup.add(item1, item2)
        return markup
    # Define function to retrieve news titles from a website
    def get_news_titles(news_site):
    
        response = requests.get(news_site)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        titles_and_links = {}
        limit=5
        for index, headline in enumerate(soup.find_all('h3')):
           title = headline.text.strip()
           link_element = headline.find('a')
           
           link = link_element['href'] if link_element else None

           titles_and_links[title] = link
           
           if index + 1 == limit:
               break
        return titles_and_links



    @bot.message_handler(func=lambda action: True)
    def echo_all(action):
        try:
            
            if action.text == "Youtube":
                
                limit_Youtube = 5
                bot.send_message(action.chat.id, "The headlines on Youtube are:")
                 # Itera a través de los resultados e imprime los títulos y URL de los vídeos
                for video in videos["items"]:
                    
                    video_title = video["snippet"]["title"]
                    video_Id = video["id"]["videoId"]
                    video_url = f"https://www.youtube.com/watch?v={video_Id}"
                    bot.send_message(action.chat.id, video_title)
                    bot.send_message(action.chat.id, video_url)

                    if limit_Youtube + 1 == limit_Youtube:
                       break
                   
                
            elif action.text == "Newspaper":
                
                bot.send_message(action.chat.id, "The headlines on the newspaper are:")
                news_site = 'https://www.lavozdemedinadigital.com/wordpress/' 
                titles = get_news_titles(news_site)
               
               
                for key, value in titles.items():
                  
                  bot.send_message(action.chat.id, key)
                  bot.send_message(action.chat.id, value)


        except:
            bot.send_message(action.chat.id, "Could you repeat")
    
    # Define function to handle /help command
    @bot.message_handler(commands=['help'])
    def help_command(message):
        cid = message.chat.id
        help_text = "The following commands are available: \n"
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
        bot.send_message(cid, help_text)
    # Start the bot
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
