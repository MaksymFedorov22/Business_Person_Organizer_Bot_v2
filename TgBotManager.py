from dotenv import set_key, get_key
import requests
import datetime
#import json

class TgBotManager:
    tgBotTOken = get_key('.env', 'TG_BOT_TOKEN1')
    baseURL = f'https://api.telegram.org/bot{tgBotTOken}/'

    def __init__(self):
        return

    def SaveMessage(self, data):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        with open("lastMessage.txt", "a", encoding="utf-8") as file:
            file.write(f"{timestamp}|{str(data)}\n")
            
    def GetUpdates(self, offset=None):
        url = self.baseURL + 'getUpdates'
        params = {'timeout': 10}
        if offset:
            params['offset'] = offset
        response = requests.get(url, params=params)
        self.SaveMessage("GetUpdates|" + str(response.content))
        return response.json()
    
    def SendMessage(self, chat_id, text):
        url = self.baseURL + 'sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        response = requests.post(url, json=payload)
        self.SaveMessage("SendMessage|" + str(response.content))

    def Start(self):
        last_update_id = None

        while True:
            updates = self.GetUpdates(last_update_id)

            if updates['result']:
                for item in updates['result']:
                    update_id = item['update_id']
                    try:
                        message = item['message']['text']
                    except:
                        message = None

                    if message:
                        chat_id = item['message']['chat']['id']
                        self.SendMessage(chat_id, f'Вы написали: {message}')

                    if last_update_id is None or update_id >= last_update_id:
                        last_update_id = update_id + 1
                        
                        
                        