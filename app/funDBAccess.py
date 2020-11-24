import requests
import json
import datetime
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

class FunDBClient:
    def __init__(self, settings): #TODO: fixme
        self.client_id = settings['client_id']
        self.client_secret = settings['client_secret']
        self.base_url = settings['address']
        self.authorize_url = 'https://account.ozma.io/auth/realms/default/protocol/openid-connect/token'
        self.check_url = '/check_access'

        self.username = settings['username']
        self.password = settings['password']

    def update_token(self):
        current_time = datetime.datetime.now().replace(microsecond=0).timestamp()
        time_left = int(self.saved_token['expires_at']) - int(current_time)
        logging.debug('Updating token expiry time to '+str(time_left))
        self.saved_token['expires_in'] = str(time_left)
        if time_left<=20:
            logging.info('Refreshing token.')
            self.start_session()

    def start_session(self):
        self.oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id))
        self.saved_token = self.oauth.fetch_token(token_url=self.authorize_url,
                username=self.username, password=self.password, client_id=self.client_id,
                client_secret=self.client_secret)
        return self.saved_token

    def check_auth(self):
        headers = {'Authorization': 'Bearer ' + self.saved_token['access_token'], 'token_type': self.saved_token['token_type']}
        url = self.base_url + self.check_url
        request = requests.get(url=url, headers=headers)
        response = request.status_code
        if response == 200:
            logging.info('Auth check passed.')
            return True
        else:
            logging.info('Got '+str(response)+' when checking access.')
            return False

    def get(self, url, params={}):
        headers = {'Authorization': 'Bearer ' + self.saved_token['access_token'], 'token_type': self.saved_token['token_type']}
        request_url = self.base_url + url

        logging.info('GET '+ request_url + ('' if params=={} else (' with params '+str(params))))

        request = requests.get(url=request_url, headers=headers, params=params)

        logging.info('Got ' + str(request.status_code))
        if request.status_code==200:
            try:
                response = request.json()
                logging.info('Got JSON from response')
                return response
            except ValueError:
                logging.error('Could not get JSON from response.')
                return None
        else:
            logging.error('Not a 200, aborting.')
            return None

    def get_view(self, view_name, schema_name, params={}):
        url = '/views/by_name/'+schema_name+'/'+view_name+'/entries'
        return self.get(url=url, params=params)

    # def post(self, url, body=''):
    #     headers = {'Authorization': 'Bearer ' + self.saved_token['access_token'], 'token_type': self.saved_token['token_type']}
    #     request_url = self.base_url + url

    #     logging.info('POST '+ request_url + ('' if body=='' else (' with body '+str(body))))

    #     request = requests.post(url=request_url, headers=headers, data=body)

    #     logging.info('Got ' + str(request.status_code))
    #     if request.status_code==200:
    #         try:
    #             response = request.json()
    #             logging.info('POST successful, got JSON reply')
    #             return response
    #         except ValueError:
    #             logging.error('Got 200, but could not get JSON from server')
    #             return None
    #     else:
    #         logging.error('Not a 200, aborting.')
    #         return None
        
    def post(self, url, body):
        headers = {'Authorization': 'Bearer ' + self.saved_token['access_token'], 'token_type': self.saved_token['token_type'],
                    'Content-type': 'application/json'}
        request_url = self.base_url + url

        logging.info('POST '+ request_url + ('' if body=={} else (' with body '+str(body))))

        request = requests.post(url=request_url, headers=headers, data=body)

        logging.info('Got ' + str(request.status_code))
        if request.status_code==200:
            try:
                response = request.json()
                logging.info('Got JSON from response')
                return response
            except ValueError:
                logging.error('Got 200, but could not get JSON from response.')
                return None
        else:
            logging.error('Not a 200, aborting.')
            return None

    def add_entry(self, table_name, schema_name, entry):
        entityRef = {'schema':schema_name, 'name':table_name}
        operation = {'type':'insert', 'entity':entityRef, 'entries':entry}
        transaction = {'operations':[operation]}

        url = '/transaction'

        return self.post(url=url, body=json.dumps(transaction))