import time
import os
import win32clipboard
curdir = os.path.dirname(__file__)
class SMetamask:
    def __init__(self, driver,cswait):
        self.driver = driver
        self.cswait = cswait
        self.count = 0
    def Login(self,wallet_pwd):
        try:
            self.driver.execute_script("window.open('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#unlock', '_blank');")
            # time.sleep(1)
            # self.driver.switch_to.window(window_name=self.driver.window_handles[+1])
            self.wait_newtab(limit_time=5)
            self.driver.refresh()
            self.cswait.send_keys_by_xpath(6,'//*[@id="password"]',wallet_pwd)
            time.sleep(1)
            self.cswait.click_by_xpath(5,'//div[@class="unlock-page"]/button[@type="submit"][not(@disabled)]')
            time.sleep(1)
            self.driver.close()
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            print('Login Metamask successfully!!!')
            return {'status':'success','message':'Login Metamask successfully!!!'}
        except:
            self.driver.close()
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            return {'status':'error','message':'Login Metamask error!!!'}
    def Confirm(self,custom_gwei = False):
        try:
            self.wait_newtab(limit_time=10)
            if custom_gwei != False:
                print('Custom gas: '+str(custom_gwei))
                input_gas = self.cswait.get_element_by_xpath(5,'//input[@class="advanced-gas-inputs__gas-edit-row__input"]')
                input_gas.clear()
                input_gas.send_keys(str(custom_gwei))
                time.sleep(.6)
            self.cswait.click_by_xpath(8,'//button[@data-testid="page-container-footer-next"][not(@disabled)]')
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            print('Confirmed')
            return {'status':'success'}
        except:
            return {'status':'error'}
    def wait_newtab(self, limit_time = 5):
        count = 0
        while count < limit_time:
            try:
                self.driver.switch_to.window(window_name=self.driver.window_handles[+1])
                return True
            except:
                time.sleep(0.1)
                count = count+0.1
                continue

    def OpenTab(self):
        try:
            self.driver.execute_script("window.open('https://api.binance.com', '_blank');")
            self.driver.switch_to.window(window_name=self.driver.window_handles[+1])
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
            return {'status':'success'}
        except:
            return {'status':'error'}
    def CloseTab(self):
        try:
            self.driver.close();
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            return {'status':'success'}
        except:
            return {'status':'error'}
    def NextWallet(self):
        try:
            self.driver.execute_script("window.open('https://api.binance.com', '_blank');")
            self.driver.switch_to.window(window_name=self.driver.window_handles[+1])
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
            self.cswait.click_by_xpath(10,'//div[@class="identicon__address-wrapper"]')
            list_accounts = self.cswait.get_element_by_xpath(10,'//div[@class="account-menu__accounts"]')
            current_accounts = list_accounts.find_element_by_xpath('//div[@class="account-menu__account account-menu__item--clickable"][.//*[@class="account-menu__check-mark-icon"]]')
            list_accounts = list_accounts.find_elements_by_xpath('./div[@class="account-menu__account account-menu__item--clickable"]')
            current_wallet = list_accounts.index(current_accounts)
            list_accounts[current_wallet+1].click()
            time.sleep(1)
            self.driver.close();
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            return {'status':'success'}
        except:
            self.driver.close();
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            return {'status':'error'}
    def PrevWallet(self):
        try:
            self.driver.execute_script("window.open('https://api.binance.com', '_blank');")
            self.driver.switch_to.window(window_name=self.driver.window_handles[+1])
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
            self.cswait.click_by_xpath(10,'//div[@class="identicon__address-wrapper"]')
            list_accounts = self.cswait.get_element_by_xpath(10,'//div[@class="account-menu__accounts"]')
            current_accounts = list_accounts.find_element_by_xpath('//div[@class="account-menu__account account-menu__item--clickable"][.//*[@class="account-menu__check-mark-icon"]]')
            list_accounts = list_accounts.find_elements_by_xpath('./div[@class="account-menu__account account-menu__item--clickable"]')
            current_wallet = list_accounts.index(current_accounts)
            list_accounts[current_wallet-1].click()
            time.sleep(1)
            self.driver.close();
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            return {'status':'success'}
        except:
            self.driver.close();
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            pass
    def append_new_line(self,file_name, text_to_append):
        with open(file_name, "a+") as file_object:
            file_object.seek(0)
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            file_object.write(text_to_append)
    def NextWalletCurrentTab(self):
        try:
            self.cswait.click_by_xpath(10,'//div[@class="identicon__address-wrapper"]')
            list_accounts = self.cswait.get_element_by_xpath(10,'//div[@class="account-menu__accounts"]')
            current_accounts = list_accounts.find_element_by_xpath('//div[@class="account-menu__account account-menu__item--clickable"][.//*[@class="account-menu__check-mark-icon"]]')
            list_accounts = list_accounts.find_elements_by_xpath('./div[@class="account-menu__account account-menu__item--clickable"]')
            current_wallet = list_accounts.index(current_accounts)
            print('Wallet index: '+str(current_wallet+1))
            if current_wallet == len(list_accounts) - 1:
                return 'end'
            list_accounts[current_wallet+1].click()
            return {'status':'success','index':current_wallet}
        except:
            return {'status':'error'}
    def PrevWalletCurrentTab(self):
        try:
            self.cswait.click_by_xpath(10,'//div[@class="identicon__address-wrapper"]')
            list_accounts = self.cswait.get_element_by_xpath(10,'//div[@class="account-menu__accounts"]')
            current_accounts = list_accounts.find_element_by_xpath('//div[@class="account-menu__account account-menu__item--clickable"][.//*[@class="account-menu__check-mark-icon"]]')
            list_accounts = list_accounts.find_elements_by_xpath('./div[@class="account-menu__account account-menu__item--clickable"]')
            current_wallet = list_accounts.index(current_accounts)
            print('Wallet index: '+str(current_wallet+1))
            if current_wallet == len(list_accounts) - 1:
                return 'end'
            list_accounts[current_wallet-1].click()
            return {'status':'success','index':current_wallet}
        except:
            return {'status':'error'}
    def GetNextWalletCurrentTab(self):
        try:
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
            self.cswait.click_by_xpath(10,'//div[@class="identicon__address-wrapper"]')
            list_accounts = self.cswait.get_element_by_xpath(10,'//div[@class="account-menu__accounts"]')
            current_accounts = list_accounts.find_element_by_xpath('//div[@class="account-menu__account account-menu__item--clickable"][.//*[@class="account-menu__check-mark-icon"]]')
            list_accounts = list_accounts.find_elements_by_xpath('./div[@class="account-menu__account account-menu__item--clickable"]')
            current_wallet = list_accounts.index(current_accounts)
            print('Wallet index: '+str(current_wallet+1))
            if current_wallet == len(list_accounts) - 1:
                return 'end'
            list_accounts[current_wallet+1].click()
            self.cswait.click_by_xpath(5,'//button[@data-testid="account-options-menu-button"]')
            self.cswait.click_by_xpath(2,'//button[@data-testid="account-options-menu__account-details"]')
            wallet_address = self.cswait.get_attribute_by_xpath(5,'//div[@class="qr-code"]//input[@class="readonly-input__input"]','value')
            self.cswait.click_by_xpath(2,'//button[@data-testid="account-modal__close"]')
            return {'status':'success','index':current_wallet,'wallet':wallet_address}
        except:
            return {'status':'error'}
    def GetPrevWalletCurrentTab(self):
        try:
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
            self.cswait.click_by_xpath(10,'//div[@class="identicon__address-wrapper"]')
            list_accounts = self.cswait.get_element_by_xpath(10,'//div[@class="account-menu__accounts"]')
            current_accounts = list_accounts.find_element_by_xpath('//div[@class="account-menu__account account-menu__item--clickable"][.//*[@class="account-menu__check-mark-icon"]]')
            list_accounts = list_accounts.find_elements_by_xpath('./div[@class="account-menu__account account-menu__item--clickable"]')
            current_wallet = list_accounts.index(current_accounts)
            print('Wallet index: '+str(current_wallet+1))
            if current_wallet == len(list_accounts) - 1:
                return 'end'
            list_accounts[current_wallet+1].click()
            self.cswait.click_by_xpath(5,'//button[@data-testid="account-options-menu-button"]')
            self.cswait.click_by_xpath(2,'//button[@data-testid="account-options-menu__account-details"]')
            wallet_address = self.cswait.get_attribute_by_xpath(5,'//div[@class="qr-code"]//input[@class="readonly-input__input"]','value')
            self.cswait.click_by_xpath(2,'//button[@data-testid="account-modal__close"]')
            return {'status':'success','index':current_wallet,'wallet':wallet_address}
        except:
            return {'status':'error'}
    
    def BackupWithoutKey(self,filename):
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        self.count = 0
        self.runBackupWithoutKey(filename)
    def runBackupWithoutKey(self,filename):
        self.cswait.click_by_xpath(5,'//button[@data-testid="account-options-menu-button"]')
        self.cswait.click_by_xpath(2,'//button[@data-testid="account-options-menu__account-details"]')
        wallet_address = self.cswait.get_attribute_by_xpath(5,'//div[@class="qr-code"]//input[@class="readonly-input__input"]','value')
        self.cswait.click_by_xpath(5,'//button[@class="account-modal__close"]')
        wallet_path = os.path.join(curdir, filename)
        self.append_new_line(wallet_path,wallet_address)
        print('Wallet address: '+wallet_address)
        wallet = self.NextWalletCurrentTab()
        self.count = self.count+1
        if self.count>=50:
            self.count = 0
            self.driver.refresh()
        if wallet != 'end':
            self.runBackupWithoutKey(filename)
        else:
            print('Backup successfully!!!')

    def BackupWithKey(self,filename):
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        self.count = 0
        self.runBackupWithKey(filename)
    def runBackupWithKey(self,filename):
        self.cswait.click_by_xpath(5,'//button[@data-testid="account-options-menu-button"]')
        self.cswait.click_by_xpath(2,'//button[@data-testid="account-options-menu__account-details"]')
        wallet_address = self.cswait.get_attribute_by_xpath(5,'//div[@class="qr-code"]//input[@class="readonly-input__input"]','value')
        print('Wallet address: '+wallet_address)
        self.cswait.click_by_xpath(5,'//div[@class="account-modal__container"]/button[3]')
        self.cswait.send_keys_by_xpath(5,'//input[@class="export-private-key-modal__password-input"]','tuan0910')
        self.cswait.click_by_xpath(5,'//div[contains(@class,"export-private-key-modal__buttons")]/button[2][not(@disabled)]')
        wallet_key = self.cswait.get_attribute_by_xpath(5,'//div[contains(@class,"export-private-key-modal__password-display-wrapper")]/textarea','value')
        self.cswait.click_by_xpath(5,'//button[@class="account-modal__close"]')
        wallet_path = os.path.join(curdir, filename)
        self.append_new_line(wallet_path,wallet_address+"|"+wallet_key)
        wallet = self.NextWalletCurrentTab()
        self.count = self.count+1
        if self.count>=50:
            self.count = 0
            self.driver.refresh()
        if wallet != 'end':
            self.runBackupWithKey(filename)
        else:
            print('Backup successfully!!!')
    


