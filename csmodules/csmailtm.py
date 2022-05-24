#%%
import requests
import random
import time
import datetime
import dateutil.parser
from time import sleep
from requests.structures import CaseInsensitiveDict
from faker import Faker
from threading import Thread
from functools import partial
from tqdm import tqdm
fake = Faker()

class CSMAILTM:
    def __init__(self,email = None, password = None):
        self.headers = CaseInsensitiveDict()
        self.headers["content-type"] = "application/json;charset=UTF-8"
        self.email = email
        self.password = password
        self.token = None
        if self.email != None and self.password != None:
            self.token = self.get_token(self.email,self.password)

    def create_account(self,password = 'tuan0910',limit_try = 15000):
        count = 0
        
        while count < limit_try:
            try:
                print('Creating email...')
                rand_name = fake.user_name()+fake.country_code().lower()+str(random.randint(11,99))
                address = rand_name + '@pussport.com'
                url = "https://api.mail.tm/accounts"
                data = '{"address":"'+address+'","password":"'+password+'"}'
                res_json = requests.post(url, headers=self.headers, data=data).json()
                if res_json['id']:
                    print('Create email successfully: '+address)
                    return {'address':address,'password':password,'id':res_json['id']}
                else:
                    count = count+1
                    continue
            except:
                count = count+1
                print('Create email failed! Trying...')
                continue
        print('Create email Failed! End task!')
        return False

    def get_token(self, address, password):
        if self.email == None or self.password == None:
            return None
        count = 0
        while count < 30:
            try:
                url = "https://api.mail.tm/token"
                data = '{"address":"'+address+'","password":"'+password+'"}'
                res_json = requests.post(url, headers=self.headers, data=data).json()
                return res_json['token']
            except:
                count = count+1
                sleep(1)
                continue
        return None

    def new_message(self,limit_time = 30, time_ago = 300):
        try:
            if self.token == None:
                return False   
            count = 0
            ts = int(time.time())
            # pbar = tqdm(total=limit_time,ncols=70)
            # pbar.set_description(desc='Waiting mail')
            while count<=limit_time:
                messages = self.get_messages()  
                try:              
                    if len(messages) > 0:
                        msg_created = messages[0]['createdAt']
                        ts_msg_created = int(datetime.datetime.fromisoformat(msg_created).timestamp())
                        ts_time_ago = ts - time_ago
                        if ts_msg_created > ts_time_ago:
                            print('\nWait mail successfully!')
                            # pbar.close()
                            return messages[0]
                        else:
                            sleep(2)
                            # pbar.update(0.5)
                            count = count + 2
                            continue
                    else:
                        sleep(2)
                        # pbar.update(0.5)
                        count = count + 2
                        continue
                except:
                    pass
            # pbar.close()
            if count>limit_time:
                print('\nTimeout wait mail!')
                return False
        except:
            return False
    
    def search_messages(self,keyword):
        if self.token == None:
            return False
        messages = self.get_messages(self.token)
        if len(messages)==0:
            return True
        if messages:
            for message in messages:
                if keyword in message['subject'] or keyword in message['intro'] or keyword in message['from']['name'] or keyword in message['from']['address']:
                    return message['id']
        else:
            return False
        

    def get_messages(self):
        if self.token == None:
            return False
        try:
            url = "https://api.mail.tm/messages"
            self.headers["authorization"] = "Bearer "+self.token
            res_json = requests.get(url, headers=self.headers).json()
            print('Total messages: '+str(res_json['hydra:totalItems']))
            return res_json['hydra:member']
        except:
            return False

    def get_message(self,msgid, limit_try = 1):
        count = 0
        while count < limit_try:
            if self.token == None:
                print('Error get message! Missing token!')
                return False
            try:
                url = "https://api.mail.tm/messages/"+msgid
                self.headers["authorization"] = "Bearer "+self.token
                res_json = requests.get(url, headers=self.headers).json()
                requests.patch(url, headers=self.headers)
                return res_json
            except:
                print('Error get message!')
                count = count+2
            sleep(2)
        return False

    def delete_message(self,msgid):
        try: 
            if self.token == None:
                return False
            url = "https://api.mail.tm/messages/"+msgid
            self.headers["authorization"] = "Bearer "+self.token
            requests.delete(url, headers=self.headers).json()
        except:
            return False
    
    def clear_all_messages(self):
        try:
            if self.token == None:
                return False
            messages = self.get_messages()
            if len(messages)==0:
                return True
            workers = []
            for message in messages:
                msgid = message['id']
                task_del_msg = partial(self.delete_message,msgid)
                # self.delete_message(msgid)
                worker = Thread(target=task_del_msg)
                worker.start()
                workers.append(worker)
                sleep(.1)
            pbar = tqdm(total=len(messages),ncols=70)
            pbar.set_description(desc='Delete mail')
            for worker in workers:
                worker.join()
                pbar.update(1)
            pbar.close()
            print('Delete email successfully')
            return True
        except:
            return False
            


""" address = 'dfhgjdfgfd@metalunits.com'
password = 'tuan0910'
csmail = CSMAILTM(address,password)


# msg = csmail.get_message('6177dede799e2f76b7d28a23')

msg =  csmail.new_message(limit_time=10,time_ago=300)
print(msg)

msg = csmail.get_message('617c1ef6d06817a030272abd')
print(msg)


from bs4 import BeautifulSoup
from lxml import etree
soup = BeautifulSoup(msg['html'][0], "html.parser")
dom = etree.HTML(str(soup))
element = dom.xpath('//a[contains(text(),"Sign In This Device")]')
verify_code = element[0].attrib['href']
print(verify_code) """


#%%

""" 
print(msg['html'][0])

import re
code = re.search(r"Your verification code is (.*?)\.", str(msg['html'][0])).group(1)
print(code.strip()) """



