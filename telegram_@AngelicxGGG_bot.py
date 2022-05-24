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
import random
user_fake = Faker()

csconfig = CSConfig('config.ini')

cur_dir = os.path.dirname(__file__)

list_wallets_path = os.path.join(cur_dir,'data/sol_wallets.txt')
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
    def captcha_imagetotext(self,path_img):
        api_key = '64ffec5f9e804e689151418d2b454874'
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
    async def bypass_captcha(self):
        message = await self.get_latest_message(self.userbot,10,"Human verification required")
        await message.download_media(file=os.path.join(cur_dir,'./images/captcha.jpg'))
        path_img = os.path.join(cur_dir,'./images/captcha.jpg')
        captcha = self.captcha_imagetotext(path_img)
        os.remove(path_img)
        return captcha
    async def main(self):
        api = API.TelegramIOS.Generate(unique_id=self.tele_path)
        proxy_reset(self.proxy_port)
        self.client = TelegramClient(self.tele_path,api=api,proxy=("socks5", '192.168.2.100', self.proxy_port))
        async with self.client:
            lock.acquire()
            index = int(csconfig.getConfig('number','index'))
            csconfig.setConfig('number','index',str(index+1))
            lock.release()
            user = await self.client.get_me()
            self.userbot = 'AngelicxGGG_bot'
            # self.param_data = ["r06672593280"]
            self.param_data = ["r02754727080","r01445626680","r01399340570","r06365908580","r06672593280"]
            
            self.ran_param_data = choice(self.param_data)
            while True:
                try:
                    await self.client(functions.messages.StartBotRequest(bot=self.userbot,peer=self.userbot,start_param=self.ran_param_data))
                    message = await self.get_latest_message(self.userbot,10,"Enter the captcha")
                    await message.download_media(file=os.path.join(cur_dir,'./images/captcha-'+str(self.proxy_port)+'.jpg'))
                    path_img = os.path.join(cur_dir,'./images/captcha-'+str(self.proxy_port)+'.jpg')
                    captcha = self.captcha_imagetotext(path_img)
                    os.remove(path_img)
                    await self.send_message_to_bot(self.userbot,10,"Enter the captcha",captcha)
                    check_message = await self.get_latest_message(self.userbot,5,"Please complete all the tasks and submit")
                    if check_message != None:
                        print("Correct captcha !!")
                        break
                except Exception as e:
                    print(e)
                    break

            await self.join_channel("AngelicTheGame")
            await self.join_channel("airdropinspector")
            await self.join_channel("AngelicOfficial")
            await self.click_btn_message(self.userbot,10,"Continue")
            await self.click_btn_message(self.userbot,10,"Complete the tasks below!")
            await self.click_btn_message(self.userbot,10,"After joined")
            await self.send_message_to_bot(self.userbot,10,"Submit your Twitter profile link",text="https://www.twitter.com/"+str(twitter_users[index].split("/")[3]))
            await self.send_message_to_bot(self.userbot,10,"Submit your discord username",twitter_users[index].split("/")[3]+"#"+str(random.randint(0000,9999)))
            await self.click_btn_message(self.userbot,10,"After joined")
            await self.click_btn_message(self.userbot,10,"Did you perform this task")
            await self.send_message_to_bot(self.userbot,10,"Submit your YouTube username or channel link",twitter_users[index].split("/")[3])


            await self.send_message_to_bot(self.userbot,10,"Submit your Solana (SOL) wallet address",text=str(wallets[index]))


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
        print(tele_path +"|"+ str(proxy_port))
        try:
            app = AIRDROP(tele_path,proxy_port)
            asyncio.run(app.main())
        except Exception as e:
                lock.acquire()
                append_new_line(os.path.join(cur_dir, 'logs.txt'),tele_path +str(e))
                lock.release()
                continue
        
workers =[]
proxy_port = [5002,5003,5004,5005] #
for i in range(0,len(proxy_port)):
    worker = Thread(target = partial(loop_task,proxy_port[i]))
    worker.start()
    workers.append(worker)
for worker in workers:
    worker.join()
# %%
