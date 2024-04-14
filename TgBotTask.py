# 1 - /addtask <task_name>
# 2 - /adddescriptiontask <task_name> <task_description>
# 3 - /addlisttask <task_name> <task_list>

import sqlite3

class TgBotTask:
    # Basic methods
    def __init__(self, botManager):
        self.botManager = botManager
        self.conn = sqlite3.connect("test1.db")

    def InitDbTable(self, conn):
        curr = conn.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS tasks (
                                chatID INTEGER,
                                taskType INTEGER,
                                taskName TEXT NOT NULL,
                                taskDescription TEXT NOT NULL
                            );'''
        curr.execute(create_table_query)
        conn.commit()
        return 0
    
    def ResetTasks(self, msg):
        chat_id = msg['chat']['id']
        curr = self.conn.cursor()
        delete_query = "DELETE FROM tasks WHERE chatID = ?"
        curr.execute(delete_query, (chat_id,))
        self.conn.commit()
        self.botManager.SendMessage(chat_id, "Tasks reset")
        return 0
    
    def ListTasks(self, msg):
        chat_id = msg['chat']['id']
        curr = self.conn.cursor()
        select_query = "SELECT * FROM tasks WHERE chatID = ?"
        curr.execute(select_query, (chat_id, ))
        rows = curr.fetchall()
        if len(rows) == 0:
            self.botManager.SendMessage(chat_id, "No tasks found")
            return 0
        else:
            task_list = "Your tasks:\n"
            number = 0
            for row in rows:
                number += 1
                task_list += f"{number}. {row[2]}\n"
            self.botManager.SendMessage(chat_id, task_list)
        return 0
    
    def ShowTask(self, msg):
        chat_id = msg['chat']['id']
        curr = self.conn.cursor()
        select_query = "SELECT * FROM tasks WHERE chatID = ?"
        curr.execute(select_query, (chat_id,))
        rows = curr.fetchall()
        text = msg['text']
        command, *args = text.split()
        if not len(args) == 1:
            self.botManager.SendMessage(chat_id, "Please provide the task number in the format: /showtask <task_number>")
            return 0
        number = int(args[0])
        if len(rows) == 0:
            self.botManager.SendMessage(chat_id, "No tasks found")
            return 0
        else:
            if number > len(rows):
                self.botManager.SendMessage(chat_id, "Task number out of range")
                return 0
            else:
                row = rows[number-1]
                if row[1] == 1:
                    self.ShowNoDescriptionTask(chat_id, row[2])
                elif row[1] == 2:
                    self.ShowDescriptionTask(chat_id, row[2], row[3])
                elif row[1] == 3:
                    self.ShowListTask(chat_id, row[2], row[3])
        return 0
    
    def RemoveTask(self, msg):
        chat_id = msg['chat']['id']
        curr = self.conn.cursor()
        select_query = "SELECT * FROM tasks WHERE chatID = ?"
        curr.execute(select_query, (chat_id,))
        rows = curr.fetchall()
        text = msg['text']
        command, *args = text.split()
        if not len(args) == 1:
            self.botManager.SendMessage(chat_id, "Please provide the task number in the format: /removetask <task_number>")
            return 0
        number = int(args[0])
        if len(rows) == 0:
            self.botManager.SendMessage(chat_id,"No tasks found")
            return 0
        else:
            if number > len(rows):
                self.botManager.SendMessage(chat_id,"Task number out of range")
                return 0
            else:
                row = rows[number-1]
                delete_query = "DELETE FROM tasks WHERE chatID = ? AND taskType = ? AND taskName = ?"
                curr.execute(delete_query, (chat_id, row[1], row[2]))
                self.conn.commit()
                self.botManager.SendMessage(chat_id,f"Task {row[2]} removed")
        return 0
    
    def SetTask(self, chatID, taskType, taskName, taskDescription):
        curr = self.conn.cursor()
        insert_query = '''INSERT INTO tasks (chatID, taskType, taskName, taskDescription)
                            VALUES (?, ?, ?, ?)'''
        curr.execute(insert_query, (chatID, taskType, taskName, taskDescription))
        self.conn.commit()
        return 0
    
    # Task add methods
    
    def AddNoDescriptionTask(self, msg):
        chat_id = msg['chat']['id']
        text = msg['text']
        command, *args = text.split()
        if not len(args) == 1:
            self.botManager.SendMessage(chat_id, "Please provide the task name in the format: /task <task_name>")
            return 0
        taskName = args[0]
        taskDescription = ' '
        self.SetTask(chat_id, 1, taskName, taskDescription)
        self.botManager.SendMessage(chat_id, f"Task '{taskName}' added")
        return 0

    def AddDescriptionTask(self, msg):
        chat_id = msg['chat']['id']
        text = msg['text']
        command, *args = text.split()
        if len(args) < 2:
            self.botManager.SendMessage(chat_id, "Please provide the task name and description in the format: /adddescriptiontask <task_name> <task_description>")
            return 0
        taskName = args[0]
        taskDescription = ' '.join(args[1:])
        self.SetTask(chat_id, 2, taskName, taskDescription)
        self.botManager.SendMessage(chat_id, f"Task '{taskName}' with description '{taskDescription}' \nadded")
        return 0
        
    def AddListTask(self, msg):
        chat_id = msg['chat']['id']
        text = msg['text']
        command, *args = text.split()
        if len(args) < 3:
            self.botManager.SendMessage(chat_id, "Please provide the task name and description in the format: /addlisttask <task_name> <task_list>")
            return 0
        taskName = args[0]
        taskIteams = ' '.join(args[1:])
        self.SetTask(chat_id, 3, taskName, taskIteams)
        iteams = taskIteams.split(", ")
        message = f"Task '{taskName}':\n"
        number = 0
        for iteam in iteams:
            number += 1
            message += f"{number}. {iteam}\n"
        message += "added"
        self.botManager.SendMessage(chat_id, message)
        return 0
    
    # Task show methods
    
    def ShowNoDescriptionTask(self, chat_id, taskName):
        self.botManager.SendMessage(chat_id, f"Task {taskName}: NoDescription")
        return 0
    
    def ShowDescriptionTask(self, chat_id, taskName, taskDescription):
        self.botManager.SendMessage(chat_id, f"Task {taskName}:\n{taskDescription}")
        return 0
    
    def ShowListTask(self, chat_id, taskName, taskIteams):
        iteams = taskIteams.split(", ")
        message = f"Task {taskName}:\n"
        number = 0
        for iteam in iteams:
            number += 1
            message += f"{number}. {iteam}\n"
        self.botManager.SendMessage(chat_id, message)
        return 0
