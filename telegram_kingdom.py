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
        self.api_id = 17382075
        self.api_hash = '9a1257d272e72a14e47439393918cd1b'
        self.tele_path = tele_path
        self.proxy_port = proxy_port
        self.userbot = 'PKD_Airdrop_Bot' #Username Bot Airdrop
        self.param_data ='838671899' #Param Ref Here
        #https://t.me/PKD_Airdrop_Bot?start=838671899
    
    async def get_latest_message(self,username,limit_time,key_work):
        count = 0
        while count <limit_time:
            async for message in self.client.iter_messages(username,limit=1):
                if key_work in message.text:
                    print(message.text)
                    return message
                
            else:
                sleep(1)
                count += 1
    async def join_channel(self,user_channel):
        await self.client(functions.channels.JoinChannelRequest(channel=user_channel))
    async def main(self):
        proxy_reset(self.proxy_port)
        try:
            self.client = TelegramClient(self.tele_path, self.api_id, self.api_hash,proxy=("socks5", '192.168.1.40', proxy_port))
        except:
            lock.acquire()
            append_new_line(os.path.join(cur_dir, 'logs.txt'),self.tele_path)
            lock.release()
            pass
        async with self.client:
            lock.acquire()
            index = int(csconfig.getConfig('number','index'))
            csconfig.setConfig('number','index',str(index+1))
            lock.release()
            user = await self.client.get_me()
            # # Join Channel and Chat
            lock.acquire()
            await self.join_channel('PetkingdomOfficial')
            await self.join_channel('PetkingdomANN')
            await self.join_channel('airdropo')
            await self.client(functions.messages.StartBotRequest(bot=self.userbot,peer=self.userbot,start_param=self.param_data))
            lock.release()
            # ###########   
            print(twitter_users[index].split("/")[3])
            message = await self.get_latest_message(self.userbot,limit_time=5,key_work="NEW GALAXY AIRDROP")
            await message.click(0)
            message = await self.get_latest_message(self.userbot,limit_time=5,key_work="Are you ready?")
            await message.click(0)
            message = await self.get_latest_message(self.userbot,limit_time=5,key_work="Join our Telegram")
            await message.click(0)
            message = await self.get_latest_message(self.userbot,limit_time=5,key_work="Subscribe our Channel")
            await message.click(0)
            message = await self.get_latest_message(self.userbot,limit_time=5,key_work="Follow our Twitter")
            await asyncio.sleep(2)
            await self.client.send_message(self.userbot, '@'+twitter_users[index].split("/")[3])
            await asyncio.sleep(1)
            await self.client.send_message(self.userbot, twitter_users[index])
            message = await self.get_latest_message(self.userbot,limit_time=5,key_work="Join Discord")
            await message.click(0)
            message = await self.get_latest_message(self.userbot,limit_time=5,key_work="Now send your wallet")
            await asyncio.sleep(1)
            await self.client.send_message(self.userbot, wallets[index])
            message = await self.get_latest_message(self.userbot,limit_time=5,key_work="Please Submit now")
            await message.click(0)
            lock.acquire()
            print("===================================DONE "+str(user.username)+"===================================")
            append_new_line(os.path.join(cur_dir, 'result_'+str(self.userbot)+'.txt'),wallets[index]+'|'+self.tele_path)
            lock.release()
    
listdir = os.listdir('D:\Telegram_cheat')       
def loop_task(proxy_port):
    while True:
        try:
            lock.acquire()
            index_path = int(csconfig.getConfig('tele_path','index_path'))
            csconfig.setConfig('tele_path','index_path',str(index_path+1))
            lock.release()
            # tele_path = 'D:\\Telegram_cheat\\' + listdir[index_path] +'\\'+ listdir[index_path]+'.session'
            tele_path = r'D:\Telegram_cheat\+84358147962\+84358147962.session'
            print('========================================================')
            print(tele_path)
            print('========================================================')
            app = AIRDROP(tele_path,proxy_port)
            asyncio.run(app.main())
            if index_path > len(listdir):
                break
        except:
            lock.acquire()
            append_new_line(os.path.join(cur_dir, 'logs.txt'),tele_path)
            lock.release()
            pass
        
workers =[]
proxy_port = ["5009"] # ,"5006","5007","5008","5010"
for i in range(0,len(proxy_port)):
    worker = Thread(target = partial(loop_task,proxy_port[i]))
    worker.start()
    workers.append(worker)
for worker in workers:
    worker.join()
# %%
