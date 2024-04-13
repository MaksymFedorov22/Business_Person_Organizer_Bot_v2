# 0 - /timer3: Set a timer for 3 minutes.
# 1 - /planedevent <event_name> <event_date>: Set a planned event with the specified name and date.
# 2 - /dailyevent <event_name> <event_start_date> <event_time>: Set a daily event with the specified name, start date, and time.
# 3 - /weeklyevent <event_name> <event_start_date> <event_time>: Set a weekly event with the specified name, start date, and time.
# 4 - /monthlyevent <event_name> <event_start_date> <event_time>: Set a monthly event with the specified name, start date, and time.
# 5 - /yearlyevent <event_name> <event_start_date> <event_time>: Set a yearly event with the specified name, start date, and time.

import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class TgBotEvent:
    # Basic methods
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
           
    def ResetEvents(self, msg):
        chat_id = msg['chat']['id']
        curr = self.conn.cursor()
        delete_query = "DELETE FROM events WHERE chatID = ?"
        curr.execute(delete_query, (chat_id,))
        self.conn.commit()
        self.botManager.SendMessage(chat_id, "Events reset")
        return 0
    
    def ListEvents(self, msg):
        chat_id = msg['chat']['id']
        curr = self.conn.cursor()
        select_query = "SELECT * FROM events WHERE chatID = ?"
        curr.execute(select_query, (chat_id, ))
        rows = curr.fetchall()
        if len(rows) == 0:
            self.botManager.SendMessage(chat_id, "No events found")
            return 0
        else:
            event_list = "Your events:\n"
            number = 0
            for row in rows:
                number += 1
                event_list += f"{number}. {row[2]} - {row[3]}\n"
            self.botManager.SendMessage(chat_id, event_list)
        return 0
    
    def RemoveEvent(self, msg):
        chat_id = msg['chat']['id']
        curr = self.conn.cursor()
        select_query = "SELECT * FROM events WHERE chatID = ?"
        curr.execute(select_query, (chat_id,))
        rows = curr.fetchall()
        text = msg['text']
        command, *args = text.split()
        if not len(args) == 1:
            self.botManager.SendMessage(chat_id, "Please provide the event number in the format: /remove <event_number>")
            return 0
        number = int(args[0])
        if len(rows) == 0:
            self.botManager.SendMessage(chat_id,"No events found")
            return 0
        else:
            if number > len(rows):
                self.botManager.SendMessage(chat_id,"Invalid event number")
                return 0
            else:
                row = rows[number - 1]
                delete_query = "DELETE FROM events WHERE chatID = ? AND eventName = ? AND eventTime = ?"
                curr.execute(delete_query, (chat_id, row[2], row[3]))
                self.conn.commit()
                self.botManager.SendMessage(chat_id,f"Event {row[2]} removed")
        return 0
    
    def SetEvent(self, chatID, eventType, eventName, eventTime):
        curr = self.conn.cursor()
        insert_query = '''INSERT INTO events (chatID, eventType, eventName, eventTime)
                            VALUES (?, ?, ?, ?)'''
        curr.execute(insert_query, (chatID, eventType, eventName, eventTime))
        self.conn.commit()
        return 0
    
    def ProcessAllEvents(self):
        self.ProcessDailyEvents()
        self.ProcessMonthlyEvents()
        self.ProcessPlannedEvents()
        self.ProcessTimer3()
        self.ProcessWeeklyEvents()
        self.ProcessYearlyEvents()
        return 0

    # Event set methods

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
            self.botManager.SendMessage(chat_id, "Please provide the event name and date in the format: /planedevent <event_name> <event_date>")
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
    
    def SetDailyEvent(self, msg):
        chat_id = msg['chat']['id']
        text = msg['text']
        command, *args = text.split()
        if len(args) < 2:
            self.botManager.SendMessage(chat_id,"Please provide the event name, date and time in the format: /dailyevent <event_name> <event_start_date> <event_time>")
            return 0
        eventName = args[0]
        strEventDate = ' '.join(args[1:])
        try:
            eventDate = datetime.strptime(strEventDate, "%Y-%m-%d %H:%M")
            self.SetEvent(chat_id, 2, eventName, eventDate)
            self.botManager.SendMessage(chat_id,f"Daily event '{eventName}' set for {strEventDate}")
        except ValueError:
            self.botManager.SendMessage(chat_id,"Invalid date format. Please use the format: YYYY-MM-DD HH:MM")
            return 0
        return 0
    
    def SetWeeklyEvent(self, msg):
        chat_id = msg['chat']['id']
        text = msg['text']
        command, *args = text.split()
        if len(args) < 2:
            self.botManager.SendMessage(chat_id,"Please provide the event name, date and time in the format: /weeklyevent <event_name> <event_start_date> <event_time>")
            return 0
        eventName = args[0]
        strEventDate = ' '.join(args[1:])
        try:
            eventDate = datetime.strptime(strEventDate, "%Y-%m-%d %H:%M")
            self.SetEvent(chat_id, 3, eventName, eventDate)
            self.botManager.SendMessage(chat_id,f"Weekly event '{eventName}' set for {strEventDate}")
        except ValueError:
            self.botManager.SendMessage(chat_id,"Invalid date format. Please use the format: YYYY-MM-DD HH:MM")
            return 0
        return 0
    
    def SetMonthlyEvent(self, msg):
        chat_id = msg['chat']['id']
        text = msg['text']
        command, *args = text.split()
        if len(args) < 2:
            self.botManager.SendMessage(chat_id,"Please provide the event name, date and time in the format: /monthlyevent <event_name> <event_start_date> <event_time>")
            return 0
        eventName = args[0]
        strEventDate = ' '.join(args[1:])
        try:
            eventDate = datetime.strptime(strEventDate, "%Y-%m-%d %H:%M")
            self.SetEvent(chat_id, 4, eventName, eventDate)
            self.botManager.SendMessage(chat_id,f"Monthly event '{eventName}' set for {strEventDate}")
        except ValueError:
            self.botManager.SendMessage(chat_id,"Invalid date format. Please use the format: YYYY-MM-DD HH:MM")
            return 0
        return 0
    
    def SetYearlyEvent(self, msg):
        chat_id = msg['chat']['id']
        text = msg['text']
        command, *args = text.split()
        if len(args) < 2:
            self.botManager.SendMessage(chat_id,"Please provide the event name, date and time in the format: /yearlyevent <event_name> <event_start_date> <event_time>")
            return 0
        eventName = args[0]
        strEventDate = ' '.join(args[1:])
        try:
            eventDate = datetime.strptime(strEventDate, "%Y-%m-%d %H:%M")
            self.SetEvent(chat_id, 5, eventName, eventDate)
            self.botManager.SendMessage(chat_id,f"Yearly event '{eventName}' set for {strEventDate}")
        except ValueError:
            self.botManager.SendMessage(chat_id,"Invalid date format. Please use the format: YYYY-MM-DD HH:MM")
            return 0
        return 0
    
    # Event processing methods
    
    def ProcessTimer3(self):
        cursor = self.conn.cursor()
        current_time = datetime.now()
        end_of_minute = current_time.replace(second=59, microsecond=999999)
        select_query = "SELECT * FROM events WHERE eventTime < ? AND eventType = ?;"
        cursor.execute(select_query, (end_of_minute, 0))
        events = cursor.fetchall()
        for event in events:
            msg = f"Reminder for your timer3 at {event[3]}"
            self.botManager.SendMessage(event[0], msg)
            query2 = "DELETE FROM events WHERE chatID = ? AND eventType = ? AND eventName = ? AND eventTime = ?;"
            cursor.execute(query2, (event[0], event[1], event[2], event[3]))
            self.conn.commit()
        return 0

    def ProcessPlannedEvents(self):
        cursor = self.conn.cursor()
        current_time = datetime.now()
        end_of_minute = current_time.replace(second=59, microsecond=999999)
        select_query = "SELECT * FROM events WHERE eventTime < ? AND eventType = ?;"
        cursor.execute(select_query, (end_of_minute, 1))
        events = cursor.fetchall()
        for event in events:
            msg = f"Reminder for your planned event {event[2]} at {event[3]}"
            self.botManager.SendMessage(event[0], msg)
            query2 = "DELETE FROM events WHERE chatID = ? AND eventType = ? AND eventName = ? AND eventTime = ?;"
            cursor.execute(query2, (event[0], event[1], event[2], event[3]))
            self.conn.commit()
        return 0
    
    def ProcessDailyEvents(self):
        cursor = self.conn.cursor()
        current_time = datetime.now()
        end_of_minute = current_time.replace(second=59, microsecond=999999)
        select_query = "SELECT * FROM events WHERE eventTime < ? AND eventType = ?;"
        cursor.execute(select_query, (end_of_minute, 2))
        events = cursor.fetchall()
        for event in events:
            msg = f"Reminder for your daily event {event[2]} at {event[3]}"
            self.botManager.SendMessage(event[0], msg)
            eventDate = datetime.strptime(event[3], "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
            strEventDate = eventDate.strftime("%Y-%m-%d %H:%M:%S")
            self.SetEvent(event[0], event[1], event[2], strEventDate)
            query2 = "DELETE FROM events WHERE chatID = ? AND eventType = ? AND eventName = ? AND eventTime = ?;"
            cursor.execute(query2, (event[0], event[1], event[2], event[3]))
            self.conn.commit()
        return 0
    
    def ProcessWeeklyEvents(self):
        cursor = self.conn.cursor()
        current_time = datetime.now()
        end_of_minute = current_time.replace(second=59, microsecond=999999)
        select_query = "SELECT * FROM events WHERE eventTime < ? AND eventType = ?;"
        cursor.execute(select_query, (end_of_minute, 3))
        events = cursor.fetchall()
        for event in events:
            msg = f"Reminder for your weekly event {event[2]} at {event[3]}"
            self.botManager.SendMessage(event[0], msg)
            eventDate = datetime.strptime(event[3], "%Y-%m-%d %H:%M:%S") + timedelta(weeks=1)
            strEventDate = eventDate.strftime("%Y-%m-%d %H:%M:%S")
            self.SetEvent(event[0], event[1], event[2], strEventDate)
            query2 = "DELETE FROM events WHERE chatID = ? AND eventType = ? AND eventName = ? AND eventTime = ?;"
            cursor.execute(query2, (event[0], event[1], event[2], event[3]))
            self.conn.commit()
        return 0
    
    def ProcessMonthlyEvents(self):
        cursor = self.conn.cursor()
        current_time = datetime.now()
        end_of_minute = current_time.replace(second=59, microsecond=999999)
        select_query = "SELECT * FROM events WHERE eventTime < ? AND eventType = ?;"
        cursor.execute(select_query, (end_of_minute, 4))
        events = cursor.fetchall()
        for event in events:
            msg = f"Reminder for your monthly event {event[2]} at {event[3]}"
            self.botManager.SendMessage(event[0], msg)
            eventDate = datetime.strptime(event[3], "%Y-%m-%d %H:%M:%S") + relativedelta(months=+1)
            strEventDate = eventDate.strftime("%Y-%m-%d %H:%M:%S")
            self.SetEvent(event[0], event[1], event[2], strEventDate)
            query2 = "DELETE FROM events WHERE chatID = ? AND eventType = ? AND eventName = ? AND eventTime = ?;"
            cursor.execute(query2, (event[0], event[1], event[2], event[3]))
            self.conn.commit()
        return 0
    
    def ProcessYearlyEvents(self):
        cursor = self.conn.cursor()
        current_time = datetime.now()
        end_of_minute = current_time.replace(second=59, microsecond=999999)
        select_query = "SELECT * FROM events WHERE eventTime < ? AND eventType = ?;"
        cursor.execute(select_query, (end_of_minute, 5))
        events = cursor.fetchall()
        for event in events:
            msg = f"Reminder for your yearly event {event[2]} at {event[3]}"
            self.botManager.SendMessage(event[0], msg)
            eventDate = datetime.strptime(event[3], "%Y-%m-%d %H:%M:%S") + relativedelta(years=+1)
            strEventDate = eventDate.strftime("%Y-%m-%d %H:%M:%S")
            self.SetEvent(event[0], event[1], event[2], strEventDate)
            query2 = "DELETE FROM events WHERE chatID = ? AND eventType = ? AND eventName = ? AND eventTime = ?;"
            cursor.execute(query2, (event[0], event[1], event[2], event[3]))
            self.conn.commit()
        return 0
