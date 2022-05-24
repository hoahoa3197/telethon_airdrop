#%%
import os 
import requests
from time import sleep

cur_dir = os.path.dirname(__file__)
def get_status_proxy(port, ip='192.168.2.100'):
    url = "http://192.168.2.100:10000/status?proxy={"+ip+":"+str(port)+"}"
    res_json = requests.get(url).json()
    return res_json['status']

def proxy_reset(port, ip='192.168.2.100', limit_time=60):
    print('Proxy '+str(port)+' restarting...')
    url = "http://192.168.2.100:10000/reset?proxy={"+ip+":"+str(port)+"}"
    requests.get(url)
    count = 0
    while count <limit_time:
        result = get_status_proxy(port)
        if result == False:
            sleep(1)
            count += 1
        else:
            print('Proxy '+str(port)+' restart completed')
            return True

