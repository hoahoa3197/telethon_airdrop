import re
import requests
from os import environ
import threading
import time
from csmodules.anycaptcha import AnycaptchaClient, HCaptchaTaskProxyless, RecaptchaV2TaskProxyless, RecaptchaV3TaskProxyless, \
    ImageToTextTask ,RecaptchaV2Task ,HCaptchaTask , FunCaptchaProxylessTask,ZaloTask
import random



def demo_imagetotext(path_img):
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
        print("success ", result)



if __name__=="__main__":
    demo_imagetotext()