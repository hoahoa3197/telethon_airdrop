import os
import subprocess
from time import sleep
import requests
from termcolor import colored as cl
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup

def check_connect(limit_time):
    count = 0
    while count < limit_time:
        try:
            res = requests.get("https://google.com", timeout=1)
            if res.status_code == 200:
                return True
        except:
            count = count + 1

def phone3g_reconnect():
    try:
        print(cl('Phone 3G reconnecting...','blue'))
        filepath="E:\\tools\\open_airmode.bat"
        p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
        sleep(2)
        p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
        check_connect(15)
        
    except:
        pass

def kcell_connect():
    os.system('rasdial Kcell')
    
def dcom_req(opt='on'):
    res = requests.get("http://192.168.8.1/html/home.html")
    soup = BeautifulSoup(res.text, "html.parser")
    csrf_token = soup.findAll("meta", {"name" : "csrf_token"})[1]['content']
    headers = CaseInsensitiveDict()
    headers["Accept"] = "*/*"
    headers["X-Requested-With"] = "XMLHttpRequest"
    headers["__RequestVerificationToken"] = csrf_token
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    headers["Cookie"] = "SessionID="+res.cookies['SessionID']
    opt = '1' if opt == 'on' else '0'
    data = '<?xml version="1.0" encoding="UTF-8"?><request><dataswitch>'+opt+'</dataswitch></request>'
    res = requests.post("http://192.168.8.1/api/dialup/mobile-dataswitch", headers=headers, data=data)
    if res.status_code == 200:
        return True
def dcom_req_reconnect():
    print(cl('Dcom Request reconnecting...','blue'))
    dcom_req(opt='off')
    dcom_req(opt='on')
    check_connect(15)
    print(cl('Dcom Request reconnect successfully!','green'))

def kcell_disconnect():
    os.system('rasdial /disconnect')

def kcell_reconnect():
    print(cl('Kcell reconnecting...','blue'))
    kcell_disconnect()
    kcell_connect()
    check_connect(15)
    print(cl('Kcell reconnect successfully!','green'))

def reconnect(device):
    if device == 'dcom':
        kcell_reconnect()
    elif device == 'phone':
        phone3g_reconnect()
    elif device == 'dcom_req':
        dcom_req_reconnect()


# reconnect('dcom_req')




