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
from opentele.api import API


csconfig = CSConfig('config.ini')

cur_dir = os.path.dirname(__file__)

lock=Lock()
class AIRDROP:
    def __init__(self,tele_path,proxy_port):
        self.tele_path = tele_path
        self.proxy_port = proxy_port
    async def main(self):
        api = API.TelegramIOS.Generate(unique_id=self.tele_path)
        # proxy_reset(self.proxy_port)
        # try:
        self.client = TelegramClient(self.tele_path,api,proxy=("socks5", '192.168.2.100', self.proxy_port))
        async with self.client:
            user = await self.client.get_me()
            print(user.username)
        # except:
        #     lock.acquire()
        #     append_new_line(os.path.join(cur_dir, 'die.txt'),self.tele_path)
        #     lock.release()
        #     pass
listdir = os.listdir('D:\\telegram_partner') 
print("TOTAL : " +str(len(listdir)))      
def loop_task(proxy_port):
    # while True:
    #     lock.acquire()
        index_path = int(csconfig.getConfig('tele_path','index_path'))
        # if index_path > len(listdir):
        #         print("Stop Program")
        #         break
        csconfig.setConfig('tele_path','index_path',str(index_path+1))
        # lock.release()
        # try:
                # tele_path = 'D:\\telegram_partner\\' + listdir[index_path] +'\\'+ listdir[index_path]+'.session'
        tele_path = r'G:\ACC_Tele\telethon\+84815130256\+848151302z56.session'
        print(tele_path)
        app = AIRDROP(tele_path,proxy_port)
        asyncio.run(app.main())
        # except:
        #         lock.acquire()
        #         append_new_line(os.path.join(cur_dir, 'logs.txt'),tele_path)
        #         lock.release()
        #         pass
        
workers =[]
proxy_port = [5002] #
for i in range(0,len(proxy_port)):
    worker = Thread(target = partial(loop_task,proxy_port[i]))
    worker.start()
    workers.append(worker)
for worker in workers:
    worker.join()
# %%
