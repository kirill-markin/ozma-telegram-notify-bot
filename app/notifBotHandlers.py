import phoneParser

import telegram
import datetime

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
class NotifbotHandlers:
    def __init__(self, token, notificationWorker):
        self.token = token
        self.notificationWorker = notificationWorker
        pass

    def startcommand(self, update, context):
        logging.info('Got a /start command from user '+str(update.effective_user['id']))
        chat = update.effective_chat
        if self.notificationWorker.checkIfInList(update.effective_user, chat.id):
            chat.send_message(text='Здравствуйте 🖖')#, reply_markup=telegram.ReplyKeyboardMarkup(keyboard=[[telegram.KeyboardButton(text='Ну и как там в Египте?')]]))
        else:
            chat.send_message(text='Вас нет в моих списках 😔\nОбратитесь к системному администратору, пожалуйста.')

    def send_message(self, chat_id, message):
        logging.info('Sending a message to chat '+str(chat_id))
        try:
            telegram.Chat(id=chat_id, type='private', bot=telegram.Bot(self.token)).send_message(text=message)  # was I high when I wrote this? TODO: fix
        except telegram.error.Unauthorized:
            logging.warning('Bot was blocked by the user?')
