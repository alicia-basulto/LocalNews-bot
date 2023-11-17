# Local News Bot
LocalNews bot is a project that arose as an idea to improve my python skills and at the same time to solve a need I had. To have a custom bot that would send you a message every time a new headline is published in the local newspaper you like the most. 
This is a Telegram bot that fetches and sends local news headlines to users. It supports fetching headlines from a news website as well as a YouTube channel.
Si quieres resetear el Bot comand /start @LocalNewsBot

### ⚠️ Bot is currently not deployed ⚠️
<p align="center">
<img style="display: block; margin: 0 auto;" src="https://github.com/alicia-basulto/LocalNews-bot/assets/37553654/92539c7e-fe2a-43f7-bbe8-19ac7e407dd9" alt="Logo de mi proyecto" width="50%" />
</p>
### Authors
* Alicia Basulto

### Configuration
Language: python 
Version: python3 

### Running the program

### Useful Links
* This is the article that I used to manage all the sensitive data associated with the bot API: https://blog.gitguardian.com/how-to-handle-secrets-in-python/




## Features

- Fetches recent headlines from a configured news website
- Fetches recent video titles from a specified YouTube channel
- Sends headlines to users via Telegram bot

## Usage

The bot is designed to work with Telegram. Users can interact with it by sending commands:

- `/start` - Starts the bot and sends a welcome message
- `/help` - Displays available commands

The bot provides inline buttons to choose between getting news from the website or YouTube channel. 

## Configuration

The following configuration is required:

- Telegram bot API token 
- YouTube API key
- News website URL
- YouTube channel username

Configuration is done via environment variables.

## Code Overview


#### Libraries:
It imports several libraries such as requests:
 * BeautifulSoup
 * telegram
 * dotenvbot
 * logger
 * googleapiclient.discovery.
* telebot
* requests
- `telebot` is used to interact with Telegram Bot API
- `googleapiclient` is used to fetch YouTube video data
- `beautifulsoup4` is used to scrape and parse news website
- Headlines are fetched from configured sources and sent to users
#### Tasks:
 The script performs the following tasks:
1. It loads the environment variables using the load_dotenv() function from the dotenv library.
2. It retrieves the YouTube API token from the environment variables using os.getenv("API_YOUTUBE").
3. It creates a YouTube API client using the googleapiclient.discovery.build() function.
4. It retrieves the ID of a YouTube channel based on its username using the youtube.channels().list() function.
5. It retrieves a list of videos from the YouTube channel using the youtube.search().list() function.
6. It prints the titles of the videos to the console.
7. It retrieves the Telegram Bot API token from the environment variables using os.getenv("API_SECRET").
8. It creates a Telegram bot instance using the telebot.TeleBot() function.
9.It defines several functions to handle different types of user input.
10. It defines a function to send a message to the Telegram chat using the context.bot.send_message() function.
11. It defines a function to scrape and send new notices from a webpage to the Telegram chat.
12. t starts the Telegram bot using the bot.polling() function.

## License

[MIT](LICENSE)
