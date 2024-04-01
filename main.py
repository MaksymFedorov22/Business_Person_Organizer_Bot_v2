import TgBotManager
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("test1.db")

bot1 = TgBotManager.TgBotManager()

def MessageHandler(updates):
    if updates['result']:
        for item in updates['result']:
            try:
                message = item['message']['text']
            except:
                message = None

            if message:
                chat_id = item['message']['chat']['id']
                bot1.SendMessage(chat_id, f'Вы написали: {message}')

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

def setTimer3(chat_id):
    currTime = datetime.now()
    alarmTime = currTime + timedelta(minutes=3)
    SetEvent(chat_id, 0, "timer3", alarmTime)
    bot1.SendMessage(chat_id, "Timer set")
    
def checkTimer(chat_id, conn):
    cursor = conn.cursor()

    current_time = datetime.now()
    start_of_minute = current_time.replace(second=0, microsecond=0)
    end_of_minute = start_of_minute + timedelta(minutes=1)

    select_query = '''SELECT * FROM events
                    WHERE eventTime >= ? AND eventTime < ?;'''

    cursor.execute(select_query, (start_of_minute, end_of_minute))

    events = cursor.fetchall()

    for event in events:
        bot1.SendMessage(chat_id, "Timer")

def MessageEvent(updates):
    if updates['result']:
        for item in updates['result']:
            try:
                message = item['message']['text']
            except:
                message = None

            if message == "/timer3":
                chat_id = item['message']['chat']['id']
                setTimer3(chat_id)                
            else:
                chat_id = item['message']['chat']['id']
                bot1.SendMessage(chat_id, 'incorrect command')

    return 0

def main():
    InitDb(conn)
    bot1.SetLoop(MessageHandler)
    bot1.Start()

if __name__ == '__main__':
    main()
    