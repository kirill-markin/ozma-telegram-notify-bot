from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters, MergedFilter, InvertedFilter

from notifBotHandlers import NotifbotHandlers
from funDBAccess import FunDBClient
from notificationWorker import NotificationWorker

import datetime
import time
import threading

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class notifbot:
    def __init__(self, settings, requestArgs = {}):
        logging.info('dividing settings...')
        tg_settings = {'token': settings['token']}
        logging.info('Telegram settings: ' + str(tg_settings))
        db_settings = { 'address': settings['db_address'], 'username': settings['db_username'], 'password': settings['db_password'],
                        'client_id': settings['db_client_id'], 'client_secret': settings['db_client_secret'], 'view': settings['db_view_name'],
                        'schema': settings['db_schema_name']}
        logging.info('Database settings: ' + str(db_settings))
        bot_settings = {'bot_update_time': settings['bot_update_time'], 'bot_notification_time': settings['bot_notification_time']}
        logging.info('Bot settings: ' + str(bot_settings))

        self.notificationWorker = NotificationWorker(settings['notification_list'], settings['bot_notification_time'])

        logging.info('People to notify: ' + str(self.notificationWorker.getList()))
        logging.info('ChatIds to notify: ' + str(self.notificationWorker.getChatIds()))

        ####
        #logging.info('Testing chat id replacement:')
        #self.notificationWorker.checkIfInList(500, 123)
        ####

        self.update_time = int(bot_settings['bot_update_time'])
        self.notify_time = datetime.time.fromisoformat(bot_settings['bot_notification_time'])

        self.view_name = db_settings['view']
        self.schema_name = db_settings['schema']

        logging.info('creating updater')
        self.updater = Updater(token=tg_settings['token'], request_kwargs=requestArgs, use_context=True)
        
        logging.info('creating handler and db-worker objects')
        self.dbclient = FunDBClient(db_settings)
        self.notifbotHandlers = NotifbotHandlers(tg_settings['token'], self.notificationWorker)
        self.notificationWorker.setSendHelper(self.notifbotHandlers)

        logging.info('registering handlers')
        self.updater.dispatcher.add_handler(CommandHandler('start', self.notifbotHandlers.startcommand)) # "Start" command handler
        #self.updater.dispatcher.add_handler(CommandHandler('notifyme', self.notifbotHandlers.))
        logging.info('bot init done')

        self.lastInformed = None

    def start(self):
        logging.info('starting a oauth2 session')
        token = self.dbclient.start_session()
        logging.info('got token ' + token['access_token'] + ', checking access')
        if self.dbclient.check_auth():
            logging.info('starting second thread for updating and polling')
            updater = threading.Thread(target=self.update, args=(self.update_time, ))  # Start a second thread to update the token and inform the next man in queue. TODO: 5 secs should be in a config!!
            updater.start()

            logging.info('starting bot')
            self.updater.start_polling()
        else:
            logging.error('Auth check did not pass, not continuing...')
    
    def update(self, delay):
        while True:
            time.sleep(delay)
            self.dbclient.update_token()

            if self.notificationWorker.checkTime():
                queryResult = self.dbclient.get_view(self.view_name, self.schema_name)

                cell_0_0 = queryResult['result']['rows'][0]['values'][0]['value']
                if cell_0_0 is None:
                    cell_0_0 = 0

                msg = (
                    "Доброе утро! 🔆"
                    +"\n"
                    +"\n" + "Вот ваши значения из юзервью в ячейке с адресом [0,0]: " + str(cell_0_0)
                    +"\n"
                    +"\nПродуктивного дня 💪"
                )

                self.notificationWorker.advanceTimeAndNotify(msg)
