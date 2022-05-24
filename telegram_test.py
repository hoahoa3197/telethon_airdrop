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
from csmodules.anycaptcha import AnycaptchaClient,ImageToTextTask
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
    def captcha_imagetotext(self,path_img):
        api_key = 'bbfa86831c0c46d5ac900814ee03887a'
        captcha_fp = open(os.path.join(cur_dir, path_img), 'rb')
        client = AnycaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        job = client.createTask(task,typecaptcha="text")
        job.join()
        result = job.get_solution_response()
        if result.find("ERROR") != -1:
            print("error ", result)
        else:
           return result
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
    async def bypass_captcha(self):
        message = await self.get_latest_message(self.userbot,10,"Human verification required")
        await message.download_media(file=os.path.join(cur_dir,'./images/captcha.jpg'))
        path_img = os.path.join(cur_dir,'./images/captcha.jpg')
        captcha = self.captcha_imagetotext(path_img)
        os.remove(path_img)
        return captcha
    async def main(self):
        api = API.TelegramIOS.Generate(unique_id=self.tele_path)
        self.client = TelegramClient(self.tele_path,api=api,proxy=("socks5", '192.168.1.10', self.proxy_port))
        async with self.client:
            lock.acquire()
            index = int(csconfig.getConfig('number','index'))
            csconfig.setConfig('number','index',str(index+1))
            lock.release()
            user = await self.client.get_me()
            self.userbot = 'Mstation_BSCS_Bot'
            self.param_data = ["838671899"]
            # self.param_data = ["REF838671899","REF1669520840","REF1786505889","REF1716370505","REF1767186545","REF1732043675","REF1763713191","REF1775356350","REF1716365481","REF1763594599","REF1713699579"]
            self.ran_param_data = choice(self.param_data)
            while True:
                await self.client(functions.messages.StartBotRequest(bot=self.userbot,peer=self.userbot,start_param=self.ran_param_data))
                message = await self.get_latest_message(self.userbot,10,"Human verification required")
                await message.download_media(file=os.path.join(cur_dir,'./images/captcha'+self.proxy_port+'.jpg'))
                path_img = os.path.join(cur_dir,'./images/captcha'+self.proxy_port+'.jpg')
                captcha = self.captcha_imagetotext(path_img)
                os.remove(path_img)
                await self.send_message_to_bot(self.userbot,10,"Human verification required",captcha)
                check_message = await self.get_latest_message(self.userbot,5,"Please complete the following tasks")
                if check_message.text:
                    print("Correct captcha !!")
                    break
            await self.join_channel("mstation_bscs")
            await self.join_channel("mstation_official")
            await self.click_btn_message(self.userbot,10,"Please complete the following tasks.",5)
            await self.send_message_to_bot(self.userbot,10,"twitter username",text="@"+str(twitter_users[index].split("/")[3]))
            await self.send_message_to_bot(self.userbot,10,"wallet address",text=str(wallets[index]))

            
                   


    
listdir = os.listdir(r'D:\\telegram_partner') #telegram_partner|telegram_ref  
def loop_task(proxy_port):
        tele_path = r'D:\telegram_ref\+84337520422\+84337520422.session'
        app = AIRDROP(tele_path,proxy_port)
        asyncio.run(app.main())
     
workers =[]
proxy_port = [5001] #,5002,5003,5004,5005,5006,5007,5008,5009,5010,5012,5013,5014,5015
for i in range(0,len(proxy_port)):
    worker = Thread(target = partial(loop_task,proxy_port[i]))
    worker.start()
    workers.append(worker)
for worker in workers:
    worker.join()
# %%
