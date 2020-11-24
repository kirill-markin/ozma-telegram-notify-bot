import telegram
import json
import datetime

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class NotificationWorker:
    def __init__(self, notifyListFile, time_to_notify):
        self.notifyListFile = notifyListFile
        self.timeToNotify = datetime.datetime.strptime(time_to_notify,'%H:%M:%S')
        now = datetime.datetime.now()
        notiftime = self.timeToNotify.replace(year=now.year, month=now.month, day=now.day)
        notiftimeadj = notiftime + datetime.timedelta(days=1) if notiftime < now else notiftime
        self.timeToNotify = notiftimeadj

        logging.info('Time to notify at: '+str(self.timeToNotify))

        with open(self.notifyListFile) as fp:
            self.notifyList = json.load(fp)['list']
            logging.info('Loaded ' + str(self.notifyList))

    def setSendHelper(self, helper):
        self.helper = helper

    def setDBHelper(self, helper):
        self.dbhelper = helper
    
    def getList(self):
        return self.notifyList

    def getChatIds(self):
        chatIds = []
        for notified in self.notifyList:
            if (notified['chat_id'] != -1):
                chatIds.append(notified['chat_id'])
        return chatIds

    def checkIfInList(self,telegramUser, chatId):
        logging.info('Checking if user ' + str(telegramUser) + " is in our list...")
        for notified in self.notifyList:
            if(self.checkForMatch(telegramUser, chatId, notified)):
                logging.info('Match found!')
                return True
        logging.warning('No match!')
        return False

    def checkForMatch(self,telegramUser, chatId, notified):
        if( self.checkChatId(chatId, notified) or self.checkUserId(telegramUser, chatId, notified) or
            self.checkUsername(telegramUser, chatId, notified)):# or self.checkPhone(telegramUser, chatId, notified)):  # Телефон не придумал, как сделать.
                return True
        return False

    def checkChatId(self,chatId, notified):
        if(chatId == notified['chat_id']):
            return True
        return False

    def checkUserId(self,telegramUser, chatId, notified):
        if(telegramUser.id == notified['tg_id']):
            if (notified['chat_id'] == -1):
                self.writeDownChatId(notified, chatId)
            return True
        return False

    def checkUsername(self,telegramUser, chatId, notified):
        if(telegramUser.username == notified['tg_username']):
            logging.info(chatId)
            if (notified['chat_id'] == -1):
                self.writeDownChatId(notified, chatId)
            return True
        return False

    def checkPhone(self,telegramUser, chatId, notified):
        if(telegramUser == notified['phone']):
            logging.info(chatId)
            if (notified['chat_id'] == -1):
                self.writeDownChatId(notified, chatId)
            return True
        return False

    def writeDownChatId(self,notified, chatId):
        logging.info('Replacing non-existent chat id for user ' + str(notified) + ' with ' + str(chatId))

        notifiedModified = notified
        notifiedModified['chat_id'] = chatId

        notifyListModified = [notifiedModified if x==notified else x for x in self.notifyList]
        self.notifyList = notifyListModified

        jsonToWrite = {'list': self.notifyList}
        with open(self.notifyListFile, 'w') as fp:
            json.dump(jsonToWrite, fp)
            logging.info('New list: ' + str(self.notifyList))

    def notifyValidIds(self, message):
        logging.info('Notifying valid IDs: ' + str(self.getChatIds()))
        idList = self.getChatIds()
        for chatId in idList:
            self.notifyId(chatId, message)

    def notifyId(self, chatId, message):
        logging.info('Notifying chat id ' + str(chatId))
        self.helper.send_message(chatId, message)

    def checkTime(self):
        now = datetime.datetime.now()
        logging.info('Current time is ' + str(now))
        if now > self.timeToNotify:
            return True
        else:
            return False

    def advanceTimeAndNotify(self,message):
        self.timeToNotify = self.timeToNotify + datetime.timedelta(days=1)
        self.notifyValidIds(message)
        logging.info('Notified everyone, next notif time is ' + str(self.timeToNotify))