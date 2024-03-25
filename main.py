import telebot
from dotenv import load_dotenv
import os

load_dotenv()

TgBotToken = os.getenv('TG_BOT_TOKEN1')

TgBot = telebot.TeleBot(TgBotToken)

# Функція для обробки команди /start
@TgBot.message_handler(commands=['start'])
def handle_start(message):
    TgBot.send_message(message.chat.id, "Привіт! Я твій особистий органайзер.")

