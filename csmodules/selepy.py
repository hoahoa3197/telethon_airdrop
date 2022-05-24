import json
import os
import subprocess
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from csmodules.cswait import SWait

def fix_chrome_crashed_alert(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        data['profile']['exit_type'] = "Normal"

        os.remove(path)
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
    except:
        return False

def open_driver(chrome_profile,binary_location = None, binary_auto = False,images = True,audio = True, headless = False, chrome_agrs = None):
    driver_path = 'G:/tools/webdriver/chromedriver.exe'
    fix_chrome_crashed_alert(os.path.join(chrome_profile,r'Default\Preferences'))
    options = Options()
    img_option = 1 if images == True else 2
    prefs = {"profile.managed_default_content_settings.images": img_option}
    options.add_experimental_option("prefs", prefs)
    if headless == True:
        options.add_argument('--headless')
    # Binary location
    if binary_location != None:
        options.binary_location = binary_location
    # audio
    if audio == False:
        options.add_argument("--mute-audio")
    # Another arguments
    if chrome_agrs != None:
        options.add_argument(chrome_agrs)
    # Binary auto
    if binary_auto == True:
        chrome64_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        chrome32_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        if os.path.isfile(chrome64_path):
            options.binary_location = chrome64_path
        elif os.path.isfile(chrome32_path):
            options.binary_location = chrome32_path
        else:
            return False

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', True)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-data-dir="+chrome_profile)
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.implicitly_wait(2)
    cswait = SWait(driver)
    return (driver,cswait)

def clear_cookies(driver):
    # Clear cookie
    try:
        cswait = SWait(driver)
        driver.get("https://api.binance.com")
        btn_clear = cswait.get_element_by_xpath(5,'//img[@class="inserted-btn mtz"]')
        sleep(.5)
        btn_clear.click()
        sleep(.5)
    except:
        pass
def kill_chrome():
    subprocess.call("TASKKILL /f /im chrome.exe")
