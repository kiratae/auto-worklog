from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os

class SeleniumHelperSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SeleniumHelperSingleton, cls).__call__(*args, **kwargs)

            options = Options()
            options.add_argument("start-maximized")
            options.add_argument("disable-infobars")
            options.add_argument("--disable-extensions")
            cls._instances[cls].driver = webdriver.Chrome(executable_path=os.path.join("Driver", "chromedriver.exe"), options=options)
        return cls._instances[cls]

class SeleniumHelper(metaclass=SeleniumHelperSingleton):
    pass