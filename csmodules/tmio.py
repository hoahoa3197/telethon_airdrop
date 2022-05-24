#%%
import requests
import time
import datetime
import re
from time import sleep
from requests.structures import CaseInsensitiveDict


class CSTMIO:
    def __init__(self):
        self.mail = self.create_email()

    def create_email(self):
        try:
            url = "https://api.internal.temp-mail.io/api/v3/email/new"
            headers = CaseInsensitiveDict()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            data = '{"min_name_length":10,"max_name_length":10}'
            res_json = requests.post(url, headers=headers, data=data).json()
            return res_json['email']
        except:
            return False

    def get_messages(self):
        url = "https://api.internal.temp-mail.io/api/v3/email/"+self.mail+"/messages"
        res_json = requests.get(url).json()
        return res_json
        
    def new_message(self,limit_time = 30, time_ago = 300, msg_log = ''):
        try:
            count = 0
            ts = int(time.time())
            while count<=limit_time:
                try:   
                    messages = self.get_messages()    
                    print('Total messages '+msg_log+': '+str(len(messages)))     
                    if len(messages) > 0:
                        msg_created = messages[0]['created_at']
                        msg_created = msg_created.split('.')[0] + '+00:00'
                        ts_msg_created = int(datetime.datetime.fromisoformat(msg_created).timestamp())
                        ts_time_ago = ts - time_ago
                        if ts_msg_created > ts_time_ago:
                            print('\nWait mail successfully! '+msg_log)
                            return messages[0]['body_html']
                        else:
                            count = count + 1
                    else:
                        count = count +1
                    sleep(1)
                except:
                    count = count +1
                    sleep(1)
                    pass
        except:
            print('Error get messages '+msg_log)
            pass
        if count>limit_time:
            print('\nTimeout wait mail! '+msg_log)
        return False
        
""" csmail = CSTMIO()

print(csmail.mail)
messages = csmail.new_message(limit_time=300, time_ago=300) """
