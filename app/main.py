from notifBot import notifbot

import logging
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

requestArgs = {
    #'proxy_url': 'https://127.0.0.1:1080'
}

configfile = 'config.json'
listFile = 'list.json'

logging.info('Loading config from ' + configfile)
try:
    with open(configfile) as fp:
        settings = json.load(fp)
        logging.info('Loaded ' + str(settings))
except FileNotFoundError:
    logging.error('No config file!')
    quit()

logging.info('Loading notification list from ' + listFile)
try:
    with open(listFile) as fp:
        notifyList = json.load(fp)
except FileNotFoundError:
    logging.error('No notification list!')
    quit()

bot = notifbot(settings = settings, requestArgs=requestArgs)

bot.start()