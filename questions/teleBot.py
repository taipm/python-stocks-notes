import telegram
import random

chat_id = "1133501778"
token = "1408339597:AAEd1i444kfJa2gv1FprwirR6wTkhsWRBpo"


def send_message(text):
    try:
        telegram_notify = telegram.Bot(token)
        message = text

        telegram_notify.send_message(chat_id, text=message,
                                     parse_mode='Markdown')
    except Exception as ex:
        print(ex)


#send_test_message()
