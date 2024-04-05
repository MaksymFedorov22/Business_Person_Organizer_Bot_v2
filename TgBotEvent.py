import sqlite3
from datetime import datetime, timedelta

class TgBotEvent:
    def __init__(self, botManager):
        self.botManager = botManager
        self.conn = sqlite3.connect("test1.db")

    def InitDbTable(self, conn):
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

    def SetEvent(self, chatID, eventType, eventName, eventTime):
        curr = self.conn.cursor()
        insert_query = '''INSERT INTO events (chatID, eventType, eventName, eventTime)
                            VALUES (?, ?, ?, ?)'''
        curr.execute(insert_query, (chatID, eventType, eventName, eventTime))
        self.conn.commit()
        return 0

    def SetTimer3(self, msg):
        chat_id = msg['chat']['id']
        current_time = datetime.now()
        alarm_time = current_time + timedelta(minutes=3)
        self.SetEvent(chat_id, 0, "timer3", alarm_time)
        self.botManager.SendMessage(chat_id, "Timer set")
        return 0
        
    def SetPlannedEvent(self, msg):
        chat_id = msg['chat']['id']
        text = msg['text']
        command, *args = text.split()
        if len(args) < 2:
            self.botManager.SendMessage(chat_id, "Please provide the event name and date in the format: /planedevent <event_name>, <event_date>")
            return 0
        
        eventName = args[0]
        strEventDate = ' '.join(args[1:])
        try:
            eventDate = datetime.strptime(strEventDate, "%Y-%m-%d %H:%M")
            self.SetEvent(chat_id, 1, eventName, eventDate)
            self.botManager.SendMessage(chat_id, f"Planned event '{eventName}' set for {strEventDate}")
        except ValueError:
            self.botManager.SendMessage(chat_id, "Invalid date format. Please use the format: YYYY-MM-DD HH:MM")
            return 0

        return 0

    def CheckEvent(self):
        cursor = self.conn.cursor()
        current_time = datetime.now()
        end_of_minute = current_time.replace(second=59, microsecond=999999)
        select_query = "SELECT * FROM events WHERE eventTime < ?;"
        cursor.execute(select_query, (end_of_minute, ))
        events = cursor.fetchall()
        for event in events:
            msg = f"Reminder for your event {event[2]} at {event[3]}"
            self.botManager.SendMessage(event[0], msg)
            query2 = "DELETE FROM events WHERE chatID = ? AND eventTime = ?;"
            cursor.execute(query2, (event[0], event[3]))
            self.conn.commit()
        return 0

