#%%
from time import sleep
from minutemail import Mail

class CSMail:
    def __init__(self):
        self.mail = Mail()
    def wait_mail(self,limit_time = 30):
        count = 0
        print('Waiting mail...')
        while count<=limit_time:
            if self.mail.new_message():
                body_mail = self.mail.fetch_message()
                result = body_mail[0]['bodyHtmlContent']
                print('Wait mail completed!')
                return result
            else:
                sleep(0.5)
                count = count + 0.5
                continue
        if count>limit_time:
            print('Timeout wait mail!')
            return None



# csmail = CSMail()
# print(csmail.mail)
# #%%
# csmail.wait_mail()

