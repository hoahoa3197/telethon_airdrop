from time import sleep
class antiCF:
    def __init__(self, driver, cswait):
        self.driver = driver
        self.cswait = cswait
    def get_antidetect(self, url):
            self.driver.get(url)
            self.driver.execute_script('window.open("'+url+'", "_blank").focus();')
            sleep(1)
            self.driver.switch_to.window(window_name= self.driver.window_handles[0])
            self.driver.close()
            self.driver.switch_to.window(window_name= self.driver.window_handles[0])

    def access(self, url, xpath, wait_element = 5, limit_try = 10):
        self.get_antidetect(url)
        element = 'timeout'
        count = 1
        while element == 'timeout':
            element = self.cswait.get_element_by_xpath(wait_element,xpath)
            if element == 'timeout':
                count = count +1
                if count >= limit_try:
                    return False
                self.get_antidetect(url)
        print('Success after '+str(count)+' times')
        return element