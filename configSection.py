import configparser
import os

class ConfigSectionData():
    def __init__(self, worklog, hrm):
        self.worklog = worklog
        self.hrm = hrm

class WorkLogConfigSection():
    def __init__(self, url, username, password, name):
        self.url = url
        self.username = username
        self.password = password
        self.name = name

class HRMConfigSection():
    def __init__(self, url, email, password):
        self.url = url
        self.email = email
        self.password = password

class ConfigSectionSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ConfigSectionSingleton, cls).__call__(*args, **kwargs)

            print("\> ConfigSection:: Reading config file")
            config = configparser.ConfigParser()
            config.read(os.path.join("config.ini"), encoding="UTF-8")

            wlConfig = config["WorkLog"]
            url = wlConfig['Url']
            username = wlConfig['Username']
            password = wlConfig['Password']
            name = wlConfig['Name']
            wlConfigData = WorkLogConfigSection(url, username, password, name)

            hrmConfig = config["HRM"]
            url = hrmConfig['Url']
            email = hrmConfig['Email']
            password = hrmConfig['Password']
            hrmConfigData = HRMConfigSection(url, email, password)

            cls._instances[cls] = ConfigSectionData(wlConfigData, hrmConfigData)

        return cls._instances[cls]

class ConfigSection(metaclass=ConfigSectionSingleton):
    pass