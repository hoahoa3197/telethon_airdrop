#%%
from telethon import functions, types
from telethon import TelegramClient, events
import os
import asyncio
from threading import Thread,Lock
from configs.cs_config import CSConfig
from csmodules.appendTextToFile import append_new_line
from csmodules.xproxy import proxy_reset
from time import sleep
from functools import partial
from faker import Faker
from random import choice
from opentele.api import API
user_fake = Faker()

csconfig = CSConfig('config.ini')

cur_dir = os.path.dirname(__file__)

list_wallets_path = os.path.join(cur_dir,'data/wallets.txt')
wallets = []
with open(list_wallets_path) as file_in:
    for line in file_in:
        address = line.split('|')[0]
        wallets.append(address)
 
twitter_users_path = os.path.join(cur_dir,'data/twitters_list.txt')
twitter_users = []
with open(twitter_users_path) as file_in:
    for line in file_in:
        twitter_users.append(line.strip())
lock=Lock()
class AIRDROP:
    def __init__(self,tele_path,proxy_port):
        self.tele_path = tele_path
        self.proxy_port = proxy_port
    async def click_btn_message(self,username,limit_time,keyword,position=0):
        count = 0
        while count <limit_time:
            async for message in self.client.iter_messages(username,limit=1):
                if keyword in message.text:
                    await message.click(position)
                    print("Click message done !!")
                    return 
                sleep(1)
                count += 1
        else:
            print("Not found message !!")
    async def send_message_to_bot(self,username,limit_time,keyword,text):
        count = 0
        while count <limit_time:
            async for message in self.client.iter_messages(username,limit=1):
                if keyword in message.text:
                    await asyncio.sleep(1)
                    await self.client.send_message(username, text)
                    print("Send message done !!")
                    return 
                sleep(1)
                count += 1
        else:
            print("Not found message !!")
                            
                
    async def get_latest_message(self,username,limit_time,keyword):
        count = 0
        while count <limit_time:
            async for message in self.client.iter_messages(username,limit=1):
                if keyword in message.text:
                    print(message.text)
                    return message 
                sleep(1)
                count += 1
    async def join_channel(self,user_channel):
        await self.client(functions.channels.JoinChannelRequest(channel=user_channel))
    async def main(self):
        api = API.TelegramIOS.Generate(unique_id=self.tele_path)
        proxy_reset(self.proxy_port)
        self.client = TelegramClient(self.tele_path,api=api,proxy=("socks5", '192.168.1.10', self.proxy_port))
        async with self.client:
            lock.acquire()
            index = int(csconfig.getConfig('number','index'))
            csconfig.setConfig('number','index',str(index+1))
            lock.release()
            user = await self.client.get_me()
            self.userbot = 'OasisSwapAirdropBot'
            # self.param_data = ["838671899"]
            self.param_data = ["838671899","1669520840","1786505889","1716370505","1767186545","1732043675","1763713191","1775356350","1716365481","1763594599","1713699579"]

            self.ran_param_data = choice(self.param_data)
            await self.client(functions.messages.StartBotRequest(bot=self.userbot,peer=self.userbot,start_param=self.ran_param_data))
            # Captcha
            message =  await self.get_latest_message(self.userbot,limit_time=5,keyword='Welcome to our community, please first prove me that you are a human by solving this simple math task')
            messages = message.text.split(":")
            formula = messages[1].replace('**','').replace('=','').strip()
            result_captcha = eval(formula)
            await self.send_message_to_bot(self.userbot,limit_time=10,keyword='Welcome to our community',text = str(result_captcha))
            ###################################################
            await self.join_channel("OasisSwap_org")
            await self.join_channel("OasisSwapAnn")
            await self.join_channel("AirdropDetective")
            await self.join_channel("AirdropDetectiveTeam")
            await self.join_channel("Airdrop_Manager")
            await self.click_btn_message(self.userbot,limit_time=10,keyword='Please perform the tasks below to earn',position=6)
            
            await self.send_message_to_bot(self.userbot,limit_time=10,keyword='Please enter your E-mail address',text = user_fake.user_name()+"@gmail.com")
            await self.send_message_to_bot(self.userbot,limit_time=10,keyword='Please submit your Twitter profile link',text = 'https://twitter.com/'+str(twitter_users[index].split("/")[3]))
            await self.click_btn_message(self.userbot,limit_time=10,keyword='Discord',position=0)
            await self.send_message_to_bot(self.userbot,limit_time=10,keyword='retweet link about',text = str(twitter_users[index]))
            await self.click_btn_message(self.userbot,limit_time=10,keyword='Airdrop Detective Telegram',position=0)
            await self.send_message_to_bot(self.userbot,limit_time=5,keyword='(ROSE) wallet address',text =str(wallets[index]))
            await self.click_btn_message(self.userbot,limit_time=10,keyword='airdrop related questions',position=0)


            lock.acquire()
            print("===================================DONE "+str(user.username)+"===================================")
            append_new_line(os.path.join(cur_dir, 'result_'+str(self.userbot)+'.txt'),str(user.id)+'|'+wallets[index]+'|'+self.tele_path+'| Ref by: '+str(self.ran_param_data))
            lock.release()
    
listdir = os.listdir(r'D:\\telegram_partner') #telegram_partner|telegram_ref  
def loop_task(proxy_port):
    while True:
        lock.acquire()
        index_path = int(csconfig.getConfig('tele_path','index_path'))
        csconfig.setConfig('tele_path','index_path',str(index_path+1))
        lock.release()
        tele_path = 'D:\\telegram_partner\\' + listdir[index_path] +'\\'+ listdir[index_path]+'.session'
        print(tele_path)
        try:
            app = AIRDROP(tele_path,proxy_port)
            asyncio.run(app.main())
        except:
                lock.acquire()
                append_new_line(os.path.join(cur_dir, 'logs.txt'),tele_path)
                lock.release()
                pass
        
workers =[]
proxy_port = [5001,5002,5003,5004,5005,5006,5007,5008,5009,5010,5012,5013,5014,5015] #
for i in range(0,len(proxy_port)):
    worker = Thread(target = partial(loop_task,proxy_port[i]))
    worker.start()
    workers.append(worker)
for worker in workers:
    worker.join()
# %%
