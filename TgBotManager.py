from dotenv import set_key, get_key
import requests
import datetime

class TgBotManager:
    tgBotTOken = get_key('.env', 'TG_BOT_TOKEN1')
    baseURL = f'https://api.telegram.org/bot{tgBotTOken}/'
    fnLoop = None

    def __init__(self):
        return
    
    def SetLoop(self, fnLoop):
        self.fnLoop = fnLoop
        return

    def SaveMessage(self, data):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        with open("bot.log", "a", encoding="utf-8") as file:
            file.write(f"{timestamp}|{str(data)}\n")
            
    def GetUpdates(self):
        url = self.baseURL + 'getUpdates'
        params = {'timeout': 10}
        offset = get_key('.env', 'OFFSET')
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
            updates = self.GetUpdates()
            if self.fnLoop != None:
                ret = self.fnLoop(updates)
                if ret == -1:
                    break

            if updates['result']:
                for item in updates['result']:
                    update_id = item['update_id']
                if last_update_id is None or update_id >= last_update_id:
                    last_update_id = update_id + 1
                    set_key('.env', 'OFFSET', str(last_update_id))

