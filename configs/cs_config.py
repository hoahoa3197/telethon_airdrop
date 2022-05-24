from configparser import ConfigParser
import os
class CSConfig:
    def __init__(self,cf_file):
        self.dirname = os.path.dirname(__file__)
        self.config_path = os.path.join(self.dirname, cf_file)
        if os.path.exists(self.config_path) == False:
            open(self.config_path, "w").close
        self.config = ConfigParser()
    def getConfig(self,cf_section,cf_key):
        try:
            self.config.read(self.config_path)
            self.config.sections()
            return self.config[cf_section][cf_key]
        except:
            print("Does not exist at file or section!!!")
    def setConfig(self,cf_section,cf_key,cf_value):
        try:
            if self.config.has_section(cf_section) == False:
                self.config.add_section(cf_section)
            self.config.read(self.config_path)
            self.config.sections()
            self.config.sections().append('test')
            self.config.set(cf_section,cf_key,cf_value)
            with open(self.config_path,'w') as configfile:
                self.config.write(configfile)
            return 'successful'
        except:
            print("Does not exist at file or section!!!")
# Example
# csconfig = CSConfig('test.cfg')
# csconfig.setConfig('test','key','value')