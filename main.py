import TgBotManager
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("test1.db")

bot1 = TgBotManager.TgBotManager()

commands = {}

def MessageStart(msg):
    chat_id = msg['chat']['id']
    bot1.SendMessage(chat_id, '''Hello, It is the Organizer For A Business Person Bot.
Type /timer3 to set timer for 3 minutes.''')
    return 0

def setTimer3(msg):
    chat_id = msg['chat']['id']
    currTime = datetime.now()
    alarmTime = currTime + timedelta(minutes=3)
    SetEvent(chat_id, 0, "timer3", alarmTime)
    bot1.SendMessage(chat_id, "Timer set")

def AddCommand(command, fnName):
    commands[command] = fnName
    return 0


def InitDb(conn):
    curr = conn.cursor()

    create_table_query = '''CREATE TABLE IF NOT EXISTS events (
                            chatID INTEGER,
                            eventType INTEGER,
                            eventName TEXT NOT NULL,
                            eventTime TIMESTAMP NOT NULL
                        );'''

    curr.execute(create_table_query)

    conn.commit()
    return 0

def SetEvent(chatID, eventType, eventName, eventTime):
    curr = conn.cursor()
    insert_query = '''INSERT INTO events (chatID, eventType, eventName, eventTime)
                        VALUES (?, ?, ?, ?)'''
    curr.execute(insert_query, (chatID, eventType, eventName, eventTime))
    conn.commit()
    return 0
    
def checkTimer():
    cursor = conn.cursor()
    current_time = datetime.now()
    start_of_minute = current_time.replace(second=0, microsecond=0)
    end_of_minute = current_time.replace(second=59, microsecond=999999)
    #end_of_minute = start_of_minute + timedelta(minutes=1)
    # select_query = "SELECT * FROM events WHERE eventTime >= ? AND eventTime < ?;"
    select_query = "SELECT * FROM events WHERE eventTime < ?;"
    cursor.execute(select_query, (end_of_minute, ))
    events = cursor.fetchall()
    for event in events:
        msg = f"Your timer {event[2]} at {event[3]}"
        bot1.SendMessage(event[0], msg)
        query2 = "DELETE FROM events WHERE chatID = ? AND eventTime = ?;"
        cursor.execute(query2, (event[0], event[3]))
        conn.commit()
    return

def MessageHandler(updates):
    checkTimer()
    if updates['result']:
        for item in updates['result']:
            message = item['message']['text']
            fProcessed = False
            for command, fnName in commands.items():
                if message.startswith(command):
                    fnName(item['message'])
                    fProcessed = True
                    break
            if (not fProcessed):
                chat_id = item['message']['chat']['id']
                bot1.SendMessage(chat_id, f'incorrect command {message}')
    return 0

def main():
    InitDb(conn)
    bot1.SetLoop(MessageHandler)
    AddCommand("/start", MessageStart)
    AddCommand("/timer3", setTimer3)
    #
    bot1.Start()

if __name__ == '__main__':
    main()
    