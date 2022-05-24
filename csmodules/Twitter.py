import time
import random
import json
import os
import re
from urllib.parse import urlparse
class STwitter:
    def __init__(self, driver,cswait):
        self.driver = driver
        self.cswait = cswait
    def Login(self,account,password,email):
        # try:
        self.driver.get('https://twitter.com/login?lang=en')
        print('Logging into Twitter...')
        root = self.cswait.get_element_by_xpath(5,'//div[@id="react-root"]')
        if 'https://twitter.com/login' in self.driver.current_url:
            self.cswait.send_keys_by_xpath(5,'//input[@name="session[username_or_email]"]',account)
            self.cswait.send_keys_by_xpath(5,'//input[@name="session[password]"]',password)
            time.sleep(.2)
            self.cswait.click_by_xpath(5,'//div[@data-testid="LoginForm_Login_Button"][not(@aria-disabled)]')
            tweet_btn = self.cswait.get_element_by_xpath(5,'//*[@data-testid="SideNav_NewTweet_Button"]')

            if tweet_btn != 'timeout':
                return {'status': 'success', 'message': 'Login successful!'}  
            else:
                print('Checkpoint Twitter...')
                self.cswait.send_keys_by_xpath(5,'//input[@id="challenge_response"]',email)
                self.cswait.click_by_xpath(1,'//input[@id="email_challenge_submit"][not(@aria-disabled)]')
                tweet_btn = self.cswait.get_element_by_xpath(5,'//*[@data-testid="SideNav_NewTweet_Button"]')
                if tweet_btn != 'timeout':
                    return {'status': 'success', 'message': 'Login successful!'}  
                else:
                    return {'status': 'error', 'message': 'Login failed!'} 
        else:
            self.cswait.send_keys_by_xpath(5,'//input[@name="username"]',account)
            self.cswait.click_by_xpath(5,'//div[@role="button"][.//span[contains(text(),"Next")]]')
            self.cswait.send_keys_by_xpath(5,'//input[@name="password"]',password)
            self.cswait.click_by_xpath(5,'//div[@role="button"][.//span[contains(text(),"Log in")]]')
            tweet_btn = self.cswait.get_element_by_xpath(5,'//*[@data-testid="SideNav_NewTweet_Button"]')
            if tweet_btn != 'timeout':
                return {'status': 'success', 'message': 'Login successful!'}  
            else:
                print('Checkpoint Twitter...')
                self.cswait.send_keys_by_xpath(5,'//div[@role="dialog"]//input[@name="text"][@type="email"]',email)
                self.cswait.click_by_xpath(1,'//div[@role="button"][.//span[contains(text(),"Next")]][not(@aria-disabled)]')
                tweet_btn = self.cswait.get_element_by_xpath(5,'//*[@data-testid="SideNav_NewTweet_Button"]')
                if tweet_btn != 'timeout':
                    return {'status': 'success', 'message': 'Login successful!'}  
                else:
                    return {'status': 'error', 'message': 'Login failed!'} 
            
        # except:
        #     return {'status': 'error', 'message': 'Login failed!'} 
    def LoginCookies(self,cookies):
        self.driver.get("https://api.binance.com")
        result = self.cswait.click_by_xpath(5,'//img[@class="inserted-btn mtz"]')
        if result != 'timeout':
            domain = cookies[0]['domain']
            print(domain)
            self.driver.get("https://"+domain)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            time.sleep(.5)
            self.driver.get("https://twitter.com/")
        return self.get_username()
        
    def SaveCookies(self,export_path):
        with open(export_path, 'w') as outfile:
            json.dump(self.driver.get_cookies(), outfile)

    def get_username(self):
        try:
            self.driver.get('https://twitter.com/home?lang=en')
            user = self.cswait.get_element_by_xpath(5,'//div[@data-testid="primaryColumn"]//div[./div[@role="progressbar"]]//a[@role="link"]')
            username = str(user.get_attribute('href'))
            username = urlparse(username).path
            try:
                username = username.replace('/','')
            except:
                pass
            return username
        except:
            return None

    def Follow(self,profile_link):
        if self.driver.current_url != profile_link:
            self.driver.get(profile_link)
        self.cswait.click_by_xpath(5,'//div[@role="button"][contains(@data-testid,"-follow")]')

        result = self.cswait.get_element_by_xpath(3,'//div[@role="button"][contains(@data-testid,"-unfollow")]')
        if result == 'timeout':
            self.cswait.click_by_xpath(5,'//div[@role="button"][contains(@data-testid,"-follow")]')
            result = self.cswait.get_element_by_xpath(3,'//div[@role="button"][contains(@data-testid,"-unfollow")]')
            if result == 'timeout':
                return {'status': 'error', 'message': 'Follow failed'}  
            else:
                return {'status': 'success', 'message': 'Follow successfully'}  
        else:
            return {'status': 'success', 'message': 'Follow successfully'} 
        
    def Tweet(self,content,path_image):
        try:
            path_image = r""+path_image
            path_image = re.sub(r'\\','/',path_image)
            self.driver.get('https://twitter.com') 
            self.driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]').send_keys(content) 
            self.driver.find_element_by_xpath('//*[@data-testid="fileInput"]').send_keys(path_image)
            time.sleep(1.2)
            self.driver.find_element_by_xpath('//div[@data-testid="tweetButtonInline"]').click()
            result_link = self.cswait.get_attribute_by_xpath(10,'//*[@id="layers"]//div[@data-testid="toast"]//a','href')
            result_link = result_link if result_link!= 'timeout' else 'Can not get link Tweet!'
            return {'status': 'success', 'message': 'Successful Tweet: '+result_link}  
        except:
            pass
       
    def LikeAndRetweet(self,tweet_link):
        if self.driver.current_url != tweet_link:
            self.driver.get(tweet_link)
        cards =  self.cswait.get_elements_by_xpath(5,'//div[@data-testid="tweet"]')
        main_card = cards[0]
        try:
            main_card.find_element_by_xpath('.//parent::*//div[@data-testid="like"]').click()
        except:
            pass
        try:
            main_card.find_element_by_xpath('.//parent::*//div[@data-testid="retweet"]').click()
            self.driver.find_element_by_xpath('//div[@data-testid="retweetConfirm"]').click()
        except:
            pass
        time.sleep(0.5)
        return {'status': 'success', 'message': 'Successful Like and Retweet'}

    def RetweetWithQuote(self,tweet_link,quote):
        if self.driver.current_url != tweet_link:
            self.driver.get(tweet_link)
        quote = quote+' '
        try:
            cards =  self.cswait.get_elements_by_xpath(5,'//div[@data-testid="tweet"]')
            main_card = cards[0]
            main_card.find_element_by_xpath('.//parent::*//div[contains(@data-testid,"retweet")]').click()
            self.driver.find_element_by_xpath('//div[@role="dialog"]//a[@href="/compose/tweet"]').click()
            time.sleep(0.5)
            self.cswait.send_keys_by_xpath(5,'//div[@data-testid="tweetTextarea_0"]',quote)
            self.cswait.click_by_xpath(10,'//div[@data-testid="tweetButton"]')
            result_link = self.cswait.get_attribute_by_xpath(10,'//*[@id="layers"]//div[@data-testid="toast"]//a','href')
            result_link = result_link if result_link!= 'timeout' else 'Can not get link Retweet quote!'
            return {'status': 'success', 'message': 'Successful Retweet with quote', 'link': result_link}
        except:
            return {'status': 'error', 'message': 'Error Retweet with quote tweet: '+tweet_link}
    def RetweetQuoteTagFriends(self,tweet_link,quote,num_friends):
        if self.driver.current_url != tweet_link:
            self.driver.get(tweet_link)
        quote = quote+' '
        try:
            cards = self.cswait.get_elements_by_xpath(5,'//div[@data-testid="tweet"]')
            main_card = cards[0]
            main_card.find_element_by_xpath('.//parent::*//div[contains(@data-testid,"retweet")]').click()
            self.driver.find_element_by_xpath('//div[@role="dialog"]//a[@href="/compose/tweet"]').click()
            time.sleep(0.5)
            self.cswait.send_keys_by_xpath(5,'//div[@data-testid="tweetTextarea_0"]',quote)
            # Tag friends
            list_st = ['r','t','y','p','s','d','f','g','h','j','k','l','c','v','b','n','m']
            list_nd = ['e','u','i','o','a']
            for i in range(num_friends):
                self.cswait.send_keys_by_xpath(5,'//div[@data-testid="tweetTextarea_0"]','\n@'+random.choice(list_st)+random.choice(list_nd))
                time.sleep(1.5)
                self.cswait.click_by_xpath(5,'//div[@id="typeaheadDropdownWrapped-2"]//div[@role="option"][last()]/div[@role="button"]/div/div')
            self.cswait.click_by_xpath(10,'//div[@data-testid="tweetButton"]')
            result_link = self.cswait.get_attribute_by_xpath(10,'//*[@id="layers"]//div[@data-testid="toast"]//a','href')
            result_link = result_link if result_link!= 'timeout' else 'Can not get link Retweet quote!'
            return {'status': 'success', 'message': 'Successful Retweet quote tag friends', 'link': result_link}
        except:
            return {'status': 'error', 'message': 'Error Retweet quote tag friends tweet: '+tweet_link}
        
    def Comment(self,tweet_link,content):
        if self.driver.current_url != tweet_link:
            self.driver.get(tweet_link)
        try:
            cards =  self.cswait.get_elements_by_xpath(5,'//div[@data-testid="tweet"]')
            main_card = cards[0]
            content = content + ' '
            main_card.find_element_by_xpath('.//parent::*//div[@data-testid="reply"]').click()
            time.sleep(0.5)
            self.cswait.send_keys_by_xpath(5,'//div[@data-testid="tweetTextarea_0"]',content)
            self.cswait.click_by_xpath(10,'//div[@data-testid="tweetButton"]')
            result_link = self.cswait.get_attribute_by_xpath(10,'//*[@id="layers"]//div[@data-testid="toast"]//a','href')
            result_link = result_link if result_link!= 'timeout' else 'Can not get link Retweet quote!'
            return {'status': 'success', 'message': 'Successful Comment tweet', 'link': result_link}
        except:
            return {'status': 'error', 'message': 'Error Comment tweet: '+tweet_link}
