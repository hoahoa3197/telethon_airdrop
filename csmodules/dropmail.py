import requests
from requests.structures import CaseInsensitiveDict
import time
import datetime
from time import sleep
import secrets

class DROPMAIL:
    def __init__(self):
        self.address = None
        self.session_id = None
        self.token = secrets.token_hex(25)
        self.create_email()

    def create_email(self):
        url = "https://dropmail.me/api/graphql/"+self.token
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = "query=mutation {introduceSession {id, expiresAt, addresses{id, address}}}"
        res_json = requests.post(url, headers=headers, data=data).json()
        print('New email: '+res_json['data']['introduceSession']['addresses'][0]['address'])
        self.session_id = res_json['data']['introduceSession']['id']
        self.address = res_json['data']['introduceSession']['addresses'][0]['address']
        return {'mail':res_json['data']['introduceSession']['addresses'][0]['address'], 'id': res_json['data']['introduceSession']['id']}

    def get_messages(self):
        res_json = requests.get('https://dropmail.me/api/graphql/'+self.token+'?query=query ($id: ID!) {session(id:$id) { addresses {address}, mails{rawSize,html, fromAddr, toAddr,receivedAt, downloadUrl,  headerSubject}} }&variables={"id":"'+self.session_id+'"}').json()
        return res_json

    def new_message(self, limit_time = 30, time_ago = 300, msg_log = ''):
        count = 0
        ts = int(time.time())
        while count<=limit_time:
            try:   
                messages = self.get_messages()    
                print('Total messages '+msg_log+': '+str(len(messages)))     
                if len(messages) > 0:
                    msg_created = messages['data']['session']['mails'][0]['receivedAt']
                    # msg_created = msg_created.split('.')[0] + '+00:00'
                    ts_msg_created = int(datetime.datetime.fromisoformat(msg_created).timestamp())
                    ts_time_ago = ts - time_ago
                    if ts_msg_created > ts_time_ago:
                        print('\nWait mail successfully! '+msg_log)
                        return messages['data']['session']['mails'][0]['html']
                    else:
                        count = count + 1
                else:
                    count = count +1
                sleep(1)
            except:
                count = count +1
                sleep(1)
                pass

# Example
# dp = DROPMAIL()
# new_message = dp.new_message(limit_time = 300)
# print(new_message)



# "toAddrOrig"
# "toAddr"
# "text"
# "receivedAt"
# "rawSize"
# "html"
# "headerSubject"
# "headerFrom"
# "fromAddr"


