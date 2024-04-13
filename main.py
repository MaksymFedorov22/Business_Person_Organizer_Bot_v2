import TgBotManager
import TgBotEvent
import sqlite3

conn = sqlite3.connect("test1.db")

bot1 = TgBotManager.TgBotManager()
eventManager = TgBotEvent.TgBotEvent(bot1)

commands = {}

def MessageStart(msg):
    chat_id = msg['chat']['id']
    message = '''
Hello, It is the Organizer For A Business Person Bot.
Type any of the commands to get started!
'''
    bot1.SendMessage(chat_id, message)
    MessageHelp(msg)
    return 0

def MessageHelp(msg):
    chat_id = msg['chat']['id']
    help_message = """
Available commands:
/start - Display the main menu
/planedevent <event_name> <event_date> - Set a planned event with the specified name and date
/dailyevent <event_name> <event_start_date> <event_time> - Set a daily event with the specified name, start date, and time
/weeklyevent <event_name> <event_start_date> <event_time> - Set a weekly event with the specified name, start date, and time
/monthlyevent <event_name> <event_start_date> <event_time> - Set a monthly event with the specified name, start date, and time
/yearlyevent <event_name> <event_start_date> <event_time> - Set a yearly event with the specified name, start date, and time
/reset - Reset all your events
/list - List all your events
/remove <event_number> - Remove a specific event
/help - Display this help message
"""
    bot1.SendMessage(chat_id, help_message)
    return 0

def AddCommand(command, fnName):
    commands[command] = fnName
    return 0

def InitDb(conn):
    eventManager.InitDbTable(conn)
    return 0

def GetJsonTag(json, tag):
    if json == None:
        return None
    if tag in json:
        return json[tag]
    return None

def GetJsonTagInt(json, tag0, tag1):
    return GetJsonTag(GetJsonTag(json, tag0), tag1)

def GetJsonTagInt(json, tag0, tag1, tag2):
    return GetJsonTag(GetJsonTag(GetJsonTagInt(json, tag0), tag1), tag2)

def MessageHandler(updates):
    eventManager.ProcessAllEvents()
    if GetJsonTag(updates, 'result'):
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
    AddCommand("/help", MessageHelp)
    #AddCommand("/timer3", eventManager.SetTimer3)
    AddCommand("/reset", eventManager.ResetEvents)
    AddCommand("/list", eventManager.ListEvents)
    AddCommand("/remove", eventManager.RemoveEvent)
    AddCommand("/planedevent", eventManager.SetPlannedEvent)
    AddCommand("/dailyevent", eventManager.SetDailyEvent)
    AddCommand("/weeklyevent", eventManager.SetWeeklyEvent)
    AddCommand("/monthlyevent", eventManager.SetMonthlyEvent)
    AddCommand("/yearlyevent", eventManager.SetYearlyEvent)
    #
    bot1.Start()

if __name__ == '__main__':
    main()
    