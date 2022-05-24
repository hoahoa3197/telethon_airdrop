#%%
import pyautogui
from time import sleep
from win32api import GetKeyState
from win32con import VK_CAPITAL

def mouseout():
    pyautogui.moveTo( pyautogui.size().width/2,  pyautogui.size().height) 

def pil_click_wait(limit_time,image,grayscale=False,confidence=0.9):
    mouseout()
    point = None
    search_time = 0   
    point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence)
    while point == None:
        sleep(0.2)
        search_time+=0.2
        if search_time >= limit_time:
            break
        point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence)
    if point != None:
        point_x,point_y = point
        pyautogui.click(point_x,point_y)
        return {'status':'success','x':point_x,'y':point_y}
    else:
        return {'status':'error','message':'Image not found on screen!'}
def pil_click_wait_scroll(limit_time,scroll,image,grayscale=False,confidence=0.9):
    mouseout()
    point = None
    search_time = 0   
    point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence)
    while point == None:
        sleep(0.2)
        pyautogui.scroll(scroll)
        search_time+=0.2
        if search_time >= limit_time:
            break
        point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence)
    if point != None:
        point_x,point_y = point
        pyautogui.click(point_x,point_y)
        return {'status':'success','x':point_x,'y':point_y}
    else:
        return {'status':'error','message':'Image not found on screen!'}
def pil_click_wait_region(limit_time,image,grayscale=False,confidence=0.9,left=0,top=0,width = pyautogui.size().width,height = pyautogui.size().height):
    mouseout()
    point = None
    search_time = 0   
    point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence,region = (left,top,width,height))
    while point == None:
        sleep(0.2)
        search_time+=0.2
        if search_time >= limit_time:
            break
        point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence,region = (left,top,width,height))
    if point != None:
        point_x,point_y = point
        pyautogui.click(point_x,point_y)
        return {'status':'success','x':point_x,'y':point_y}
    else:
        return {'status':'error','message':'Image not found on screen!'}
def pil_write_wait(limit_time,text,image,grayscale=False,confidence=0.9):
    mouseout()
    point = None
    search_time = 0
    point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence)
    while point == None:
        sleep(0.2)
        search_time+=0.2
        print(point)
        print(search_time)
        if search_time >= limit_time:
            break
        point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence)
    if point != None:
        point_x,point_y = point
        pyautogui.click(point_x,point_y)
        pyautogui.write(text)
        return {'status':'success','x':point_x,'y':point_y}
    else:
        return {'status':'error','message':'Image not found on screen!'}
def pil_write_wait_region(limit_time,text,image,grayscale=False,confidence=0.9,left=0,top=0,width = pyautogui.size().width,height = pyautogui.size().height):
    mouseout()
    point = None
    search_time = 0   
    point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence,region = (left,top,width,height))
    while point == None:
        sleep(0.2)
        search_time+=0.2
        if search_time >= limit_time:
            break
        point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence,region = (left,top,width,height))
    if point != None:
        point_x,point_y = point
        pyautogui.click(point_x,point_y)
        pyautogui.write(text)
        return {'status':'success','x':point_x,'y':point_y}
    else:
        return {'status':'error','message':'Image not found on screen!'}
def pil_find_wait(limit_time,image,grayscale=False,confidence=0.9):
    mouseout()
    point = None
    search_time = 0
    point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence)
    while point == None:
        sleep(0.2)
        search_time+=0.2
        print(point)
        print(search_time)
        if search_time >= limit_time:
            break
        point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence)
    if point != None:
        point_x,point_y = point
        return {'status':'success','x':point_x,'y':point_y}
    else:
        return {'status':'error','message':'Image not found on screen!'}
def pil_find_wait_region(limit_time,image,grayscale=False,confidence=0.9,left=0,top=0,width = pyautogui.size().width,height = pyautogui.size().height):
    mouseout()
    point = None
    search_time = 0   
    point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence,region = (left,top,width,height))
    while point == None:
        sleep(0.2)
        search_time+=0.2
        if search_time >= limit_time:
            break
        point = pyautogui.locateCenterOnScreen(image,grayscale=grayscale,confidence=confidence,region = (left,top,width,height))
    if point != None:
        point_x,point_y = point
        return {'status':'success','x':point_x,'y':point_y}
    else:
        return {'status':'error','message':'Image not found on screen!'}
def enable_capslock():
    if GetKeyState(VK_CAPITAL) == 0:
        pyautogui.press('capslock')
    print('Capslock is on')

def disable_capslock():
    if GetKeyState(VK_CAPITAL) == 1:
        pyautogui.press('capslock')
    print('Capslock is off')

def write(text):
    pyautogui.write(text)

def write_lower(text):
    disable_capslock()
    pyautogui.write(text)

def write_upper(text):
    enable_capslock()
    pyautogui.write(text)
    disable_capslock()













# Example
# import modules.pyautogui_image as pi
# pi.click_wait(10,'E:/py_project/Airdrop/bremit/modules/Screenshot_1.png',grayscale=True)