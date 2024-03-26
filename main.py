from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

tgBotTOken = os.getenv('TG_BOT_TOKEN1')
baseURL = f'https://api.telegram.org/bot{tgBotTOken}/'

def SaveMessage(chat_id):
    with open("lasmsg.txt", "w") as file:
        file.write(str(chat_id))

def GetUpdates(offset=None):
    url = baseURL + 'getUpdates'
    params = {'timeout': 10}
    if offset:
        params['offset'] = offset
    response = requests.get(url, params=params)
    SaveMessage(response.content)
    return response.json()

def send_message(chat_id, text):
    url = baseURL + 'sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

def main():
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)

        if updates['result']:
            for item in updates['result']:
                update_id = item['update_id']
                try:
                    message = item['message']['text']
                except:
                    message = None

                if message:
                    chat_id = item['message']['chat']['id']
                    send_message(chat_id, f'Вы написали: {message}')

                if last_update_id is None or update_id >= last_update_id:
                    last_update_id = update_id + 1

if __name__ == '__main__':
    main()
    