import telebot
from dotenv import load_dotenv
import os

load_dotenv()

tgBotToken = os.getenv('TG_BOT_TOKEN1')

TgBot = telebot.TeleBot(tgBotToken)

def SaveChatID(chat_id):
    with open("chat_id.txt", "w") as file:
        file.write(str(chat_id))
        
def LoadChatID():
    try:
        with open("chat_id.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return None

@TgBot.message_handler(commands=['start'])
def HandleStart(message):
    ChatID = message.chat.id
    SaveChatID(ChatID)
    TgBot.send_message(ChatID, "Привіт! Я твій особистий органайзер.")

TgBot.polling()

