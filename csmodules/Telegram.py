#%%
from time import sleep
import os
import re
import subprocess
import pyautogui
import win32clipboard
import csmodules.csautowin as cswin

class TelegramDesktop:
    def __init__(self,telegram_path,width=400,height=550):
        self.telegram_path = telegram_path
        self.window = -1
        self.width = width
        self.height = height
        self.cur_dir = os.path.dirname(__file__)
        self.img_path = os.path.join(self.cur_dir,'telegram_images')

    def start(self,wait = 2):
        self.kill_telegram()
        sleep(.5)
        self.app = subprocess.Popen(self.telegram_path)
        print('Start telegram successfully')
        self.get_window()
        sleep(wait)
        self.resize(self.width,self.height)
        self.move_corner()        
        
    def move_corner(self):
        self.get_window()
        if self.window != -1:
            move_left = self.window.left*(-1) if self.window.left > 0 else (0 if self.window.left == 0 else self.window.left*(-1))
            move_top = self.window.top*(-1) if self.window.top > 0 else (0 if self.window.top == 0 else self.window.top*(-1))
            self.window.move(move_left, move_top)
            return {'status':'success','message':'Move corner successfully'}
        else:
            return {'status':'error','message':'Move corner Failed'}

    def resize(self,width,height):
        width = (self.window.width-width)*(-1) if self.window.width > width else (0 if self.window.width == width else width - self.window.width)
        height = (self.window.height-height)*(-1) if self.window.height > height else (0 if self.window.height == height else height - self.window.height)
        self.window.resize(width, height)

    def show(self):
        try:
            self.window.minimize()
            sleep(.3)
            self.window.restore()
        except:
            return False

    def hide(self):
        try:
            self.window.minimize()
        except:
            return False

    def prepare_path(self,path):
        return os.path.join(self.img_path,path)

    def home(self):
        pyautogui.press('esc')
        pyautogui.press('esc')
        pyautogui.press('esc')
        check = False
        while check == False:
            menu_search = cswin.pil_find_wait_region(1,self.prepare_path('icon_menu.png'),confidence=0.85,left=0,top=0,width=275,height=self.height)
            if menu_search['status'] == 'error':
                pyautogui.press('esc')
            else:
                break
    
    def get_username(self):
        self.home()
        self.empty_clipboard()
        open_menu = cswin.pil_click_wait_region(8,self.prepare_path('icon_menu.png'), grayscale=True,confidence=0.7,left=0,top=0,width=275,height=self.height)
        sleep(.2)
        if open_menu['status'] == 'success':
            cswin.pil_click_wait_region(8,self.prepare_path('settings.png'), grayscale=True,confidence=0.7,left=0,top=0,width=275,height=self.height)
            sleep(.5)
            cswin.pil_click_wait_region(8,self.prepare_path('edit_profile.png'), grayscale=True,confidence=0.7,left=0,top=0,width=275,height=self.height)
            user_name_icon = cswin.pil_find_wait_region(8,self.prepare_path('username_icon.png'), grayscale=True,confidence=0.8,left=0,top=0,width=275,height=self.height)
            if user_name_icon['status'] == 'success':
                pyautogui.click(button='right',x=user_name_icon['x'], y=user_name_icon['y'])
                cswin.pil_click_wait_region(5,self.prepare_path('copy_username.png'), grayscale=True,confidence=0.7,left=0,top=0,width=275,height=self.height)
                username = self.get_clipboard()
                self.empty_clipboard()
                if '@' in username:
                    return username
                else:
                    return False
            else:
                return False
        else:
            return False
    def get_phone(self):
        self.home()
        self.empty_clipboard()
        open_menu = cswin.pil_click_wait_region(8,self.prepare_path('icon_menu.png'), grayscale=True,confidence=0.7,left=0,top=0,width=275,height=self.height)
        sleep(.2)
        if open_menu['status'] == 'success':
            cswin.pil_click_wait_region(8,self.prepare_path('settings.png'), grayscale=True,confidence=0.7,left=0,top=0,width=275,height=self.height)
            sleep(.5)
            cswin.pil_click_wait_region(8,self.prepare_path('edit_profile.png'), grayscale=True,confidence=0.7,left=0,top=0,width=275,height=self.height)
            phone_icon = cswin.pil_find_wait_region(8,self.prepare_path('phone_icon.png'), grayscale=True,confidence=0.8,left=0,top=0,width=275,height=self.height)
            if phone_icon['status'] == 'success':
                pyautogui.click(button='right',x=phone_icon['x'], y=phone_icon['y'])
                cswin.pil_click_wait_region(5,self.prepare_path('copy_phone.png'), grayscale=True,confidence=0.7,left=0,top=0,width=275,height=self.height)
                phone_number = self.get_clipboard()
                self.empty_clipboard()
                if '+' in phone_number:
                    return phone_number
                else:
                    return False
            else:
                return False
        else:
            return False

    def open_profile(self,profile_link,profile_image,type='group'):
        pyautogui.hotkey('ctrl','0')
        cswin.write_upper(profile_link)
        pyautogui.press('enter')

        cswin.pil_find_wait_region(4,self.prepare_path(profile_image),grayscale=True,confidence=0.85,left=0,top=85,width=self.width,height=self.height-135)

        cswin.pil_click_wait_region(10,self.prepare_path(profile_image),grayscale=True,confidence=0.85,left=0,top=85,width=self.width,height=self.height-135)

        cswin.pil_click_wait_region(4,self.prepare_path('join_'+type+'.png'),grayscale=True,confidence=0.5,left=0,top=600,width=520,height=50)
        pyautogui.click(x=self.width-145,y=self.height-50)
        pyautogui.click(x=self.width-145,y=self.height-50)
        sleep(0.5)
        if type == 'group':
            result = cswin.pil_find_wait_region(10,self.prepare_path('write_message.png'),grayscale=True,confidence=0.6,left=0,top=self.height-50,width=self.width,height=50)
            if result['status'] == 'error':
                return False
        elif type == 'channel':
            result = cswin.pil_find_wait_region(10,self.prepare_path('mute.png'),grayscale=True,confidence=0.55,left=0,top=self.height-50,width=self.width,height=50)
            if result['status'] == 'error':
                return False
        elif type == 'bot':
            pass
        sleep(0.5)
        return True

    def get_clipboard(self):
        win32clipboard.OpenClipboard()
        text = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return text

    def empty_clipboard(self):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText( '', win32clipboard.CF_TEXT )
        win32clipboard.CloseClipboard()

    def get_message(self,message_image):
        find_message = cswin.pil_find_wait_region(10,message_image, grayscale=True, confidence=0.75, left=0,top=85, width=self.width, height=self.height-135)
        if find_message['status'] == 'success':
            pyautogui.click(button='right',x=find_message['x'], y=find_message['y'])
            sleep(.2)
            cswin.pil_click_wait_region(6,self.prepare_path('copy_message.png'),grayscale=True,confidence=0.7,width=self.width+120 ,height=self.height)
            sleep(.5)
            message = self.get_clipboard()
            self.empty_clipboard()
            return message
        else:
            return False

    def get_window(self):
        try:
            self.get_tele_window = pyautogui.getWindowsWithTitle(self.get_title())
            if len(self.get_tele_window) > 0:
                self.window = self.get_tele_window[0]
            else:
                self.window = -1
        except:
            print('Get Telegram window Failed!!!')
            self.window = -1

    def get_title(self):
        count = 0
        tele_title = None
        while tele_title == None:
            if count > 15:
                break
            windows_titles = pyautogui.getAllTitles()
            for title in windows_titles:
                match = re.search('^Telegram$|^Telegram\s\(\d+\)',title)
                if match != None:
                    tele_title = match.string
            if tele_title == None:
                sleep(.5)
                count = count + 0.5
        return tele_title        

    def kill_telegram(self):
        subprocess.call(['taskkill', '/f', '/im', 'Telegram.exe'])
