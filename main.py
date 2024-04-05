import TgBotManager
import TgBotEvent
import sqlite3

conn = sqlite3.connect("test1.db")

bot1 = TgBotManager.TgBotManager()
eventManager = TgBotEvent.TgBotEvent(bot1)

commands = {}

def MessageStart(msg):
    chat_id = msg['chat']['id']
    bot1.SendMessage(chat_id, '''Hello, It is the Organizer For A Business Person Bot.
Type /timer3 to set timer for 3 minutes.''')
    return 0

def AddCommand(command, fnName):
    commands[command] = fnName
    return 0

def InitDb(conn):
    eventManager.InitDbTable(conn)
    return 0

def MessageHandler(updates):
    eventManager.CheckEvent()
    if updates['result']:
        for item in updates['result']:
            #message = item['message']['text']
            if 'message' in item:
                message = item['message']
                txtMessage = item['message']['text']
            elif 'edited_message' in item:
                message = item['edited_message']
                txtMessage = item['edited_message']['text']
            else:
                continue
            fProcessed = False
            for command, fnName in commands.items():
                if txtMessage.startswith(command):
                    fnName(message)
                    fProcessed = True
                    break
            if (not fProcessed):
                chat_id = item['message']['chat']['id']
                bot1.SendMessage(chat_id, f'incorrect command {txtMessage}')
    return 0

def main():
    InitDb(conn)
    bot1.SetLoop(MessageHandler)
    AddCommand("/start", MessageStart)
    AddCommand("/timer3", eventManager.SetTimer3)
    AddCommand("/planedevent", eventManager.SetPlannedEvent)
    #
    bot1.Start()

if __name__ == '__main__':
    main()
    