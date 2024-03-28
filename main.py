import TgBotManager

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

def main():
    bot1.SetLoop(MessageHandler)
    bot1.Start()

if __name__ == '__main__':
    main()
    