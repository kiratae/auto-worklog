from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import configparser
import time
from datetime import datetime
import xlrd
import os
from worklog import WorkLog
from hrm import HRM
from collections import defaultdict
import math
import calendar

appVersion = "0.0.1"

def main():
    print("############################")
    print("#   Auto Time-Sheet v" + appVersion + "   #")
    print("############################")

    # url, email, password = getConfig(hrmConfigSection)

    # print("E-mail :", email)

    runDate = datetime.today()

    wl = WorkLog()
    wl.login()
    tasks = wl.timelinePage(runDate)
    try:
        wl.close()
    except:
        pass

    print("\> Processing data...")
    tempProjDict = defaultdict(list)
    for t in tasks:
        tempProjDict[t.project].append(t)

    projectDict = defaultdict()
    for k, v in tempProjDict.items():
        if k != None:
            tempDateDict = defaultdict(list)
            dateDict = defaultdict(int)
            for t in v:
                tempDateDict[t.date].append(t.timeSpent)
            for k2, v2 in tempDateDict.items():
                sumDate = 0
                for ts in v2:
                    sumDate += ts
                dateDict[k2] = math.ceil(sumDate / 60)
            projectDict[k] = dateDict
    print("\> Done processing data")

    hrm = HRM()
    hrm.login()
    hrm.timeSheetListPage(runDate)
    hrm.timeSheetEditPage(runDate)

    row = 0
    for k, v in projectDict.items():
        hrm.addProjectRow(row, k, v, row > 0, runDate)
        row += 1

    hrm.saveDraftTimeSheet()

    countDownTime = 30
    for i in range(countDownTime):
        print("\> Closing in {0} s".format(countDownTime - i))
        time.sleep(1)

    try:
        hrm.close()
    except:
        pass
    exit()


main()
