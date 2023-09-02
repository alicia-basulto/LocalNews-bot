import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# local newspaper URL
url = "https://www.lavozdemedinadigital.com/wordpress/category/medina-del-campo/"

# get the HTML content
respuesta = requests.get(url)
contenido = respuesta.content

#parse html content with BeautifulSoup
soup = BeautifulSoup(contenido, "html.parser")

# Get the web title
title = soup.title.string
list = soup.findAll('div', class_='td-module-thumb')

#Print the title for each news
for element in list:
    block=element.find('a')
    result = block['title']
    print(result)
    print("-------------------------------------------------------------------")