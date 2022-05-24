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
from random import choice, randint
from opentele.api import API


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
        self.client = TelegramClient(self.tele_path,api=api,proxy=("socks5", '192.168.1.2', self.proxy_port))
        async with self.client:
            lock.acquire()
            index = int(csconfig.getConfig('number','index'))
            csconfig.setConfig('number','index',str(index+1))
            lock.release()
            user = await self.client.get_me()
            self.userbot = 'ACYFinanceAirdropbot'
            # self.param_data = ["r0807267747"]
            self.param_data = ["r0807267747","r06672593280","r02754727080","r01445626680","r01399340570","r06365908580","r02822264580","r00863044580","r00794147780","r06969827080"]
            await self.join_channel('acyfinance')
            await self.join_channel('ACYFinanceChannel')
            await self.join_channel('airdropo')
            self.ran_param_data = choice(self.param_data)
            await self.client(functions.messages.StartBotRequest(bot=self.userbot,peer=self.userbot,start_param=self.ran_param_data))
           
            # ###################################################
            await self.click_btn_message(self.userbot,limit_time=5,keyword='You must complete all task then click check button')
            await self.click_btn_message(self.userbot,limit_time=5,keyword='Join Airdrop')
            await self.click_btn_message(self.userbot,limit_time=5,keyword='Airdrop Rules')
            await self.click_btn_message(self.userbot,limit_time=5,keyword='After joined')
            await self.send_message_to_bot(self.userbot,limit_time=5,keyword='Submit your Twitter profile link',text = 'https://www.twitter.com/'+str(twitter_users[index].split("/")[3]))
            await self.send_message_to_bot(self.userbot,limit_time=5,keyword='Discord',text = str(twitter_users[index].split("/")[3]+'#'+str(randint(0000,9999))))
            await self.send_message_to_bot(self.userbot,limit_time=5,keyword='Submit your YouTube username or channel link',text = str(twitter_users[index].split("/")[3]))
            await self.send_message_to_bot(self.userbot,limit_time=5,keyword='Submit BEP20 Address',text =str(wallets[index]))
            await self.click_btn_message(self.userbot,limit_time=5,keyword='Advertiser Channel')
            await self.send_message_to_bot(self.userbot,limit_time=5,keyword='Submit your retweeted link',text =str(twitter_users[index]))
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
proxy_port = [5001,5002,5003,5004,5005,5006,5007,5008,5009,5010] #
for i in range(0,len(proxy_port)):
    worker = Thread(target = partial(loop_task,proxy_port[i]))
    worker.start()
    workers.append(worker)
for worker in workers:
    worker.join()
# %%
