import TgBotManager
import TgBotEvent
import TgBotTask
import sqlite3

conn = sqlite3.connect("bot1.db")

botManager = TgBotManager.TgBotManager()
eventManager = TgBotEvent.TgBotEvent(botManager)
taskManager = TgBotTask.TgBotTask(botManager)

commands = {}

def MessageStart(msg):
    chat_id = msg['chat']['id']
    message = """
🎉 Welcome to the Organizer Bot! 🎉

I'm here to help you stay on top of your business activities. With this bot, you can:

- Set up events, from one-time planned events to daily, weekly, monthly, and yearly recurring events
- Manage your tasks, including tasks with descriptions and task lists
- Reset your events and tasks
- List all your upcoming events and current tasks
- Remove specific events or tasks

To get started, simply type any of the available commands. You can also type /help to see the full list of commands.

Let's get organized and productive together! 💪
"""
    botManager.SendMessage(chat_id, message)
    MessageHelp(msg)
    return 0

def MessageHelp(msg):
    chat_id = msg['chat']['id']
    help_message = """
Here are the available commands:

/start - Display the main menu
/event event_name event_date - Set a planned event (event_name without spaces)
/dailyevent event_name event_start_date event_time - Set a daily event (event_name without spaces)
/weeklyevent event_name event_start_date event_time - Set a weekly event (event_name without spaces)
/monthlyevent event_name event_start_date event_time - Set a monthly event (event_name without spaces)
/yearlyevent event_name event_start_date event_time - Set a yearly event (event_name without spaces)
/resetevents - Reset all your events
/listevents - List all your events
/removeevent event_number - Remove a specific event
/task task_name - Add a new task (task_name without spaces)
/descriptiontask task_name task_description - Add a task with description (task_name without spaces)
/listtask task_name task_list - Add a task with a list of items (task_name without spaces)
/resettasks - Reset all your tasks
/listtasks - List all your tasks
/showtask task_number - Show details of a specific task
/removetask task_number - Remove a specific task
/help - Display this help message

Feel free to use any of these commands to stay organized and on top of your business activities! Remember, all names (event_name and task_name) must be provided without spaces.
"""
    botManager.SendMessage(chat_id, help_message)
    return 0


def AddCommand(command, fnName):
    commands[command] = fnName
    return 0

def InitDb(conn):
    eventManager.InitDbTable(conn)
    taskManager.InitDbTable(conn)
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
                botManager.SendMessage(chat_id, f'incorrect command {txtMessage}')
    return 0

def main():
    InitDb(conn)
    botManager.SetLoop(MessageHandler)
    # Basic commands
    AddCommand("/start", MessageStart)
    AddCommand("/help", MessageHelp)
    # Event commands
    #AddCommand("/timer3event", eventManager.SetTimer3)
    AddCommand("/resetevents", eventManager.ResetEvents)
    AddCommand("/listevents", eventManager.ListEvents)
    AddCommand("/removeevent", eventManager.RemoveEvent)
    AddCommand("/event", eventManager.SetPlannedEvent)
    AddCommand("/dailyevent", eventManager.SetDailyEvent)
    AddCommand("/weeklyevent", eventManager.SetWeeklyEvent)
    AddCommand("/monthlyevent", eventManager.SetMonthlyEvent)
    AddCommand("/yearlyevent", eventManager.SetYearlyEvent)
    # Task commands
    AddCommand("/resettasks", taskManager.ResetTasks)
    AddCommand("/listtasks", taskManager.ListTasks)
    AddCommand("/showtask", taskManager.ShowTask)
    AddCommand("/removetask", taskManager.RemoveTask)
    AddCommand("/task", taskManager.AddNoDescriptionTask)
    AddCommand("/descriptiontask", taskManager.AddDescriptionTask)
    AddCommand("/listtask", taskManager.AddListTask)
    #
    botManager.Start()

if __name__ == '__main__':
    main()
    