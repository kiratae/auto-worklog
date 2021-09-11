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
from Class.task import Task
from worklog import WorkLog

appVersion = "0.0.1"

def readTaskSheet(readDate):
    results = []
    filePath = os.path.join("TaskSheets", readDate.strftime("%Y"), readDate.strftime("%B") + ".xlsx")
    try:
        wb = xlrd.open_workbook(filePath)
        sheet = wb.sheet_by_name("Task")
        for i in range(1, sheet.nrows):
            rowData = sheet.row_values(i)
            date = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(rowData[0]) - 2)
            if date == readDate:
                results.append(Task(readDate, rowData[1], rowData[2], rowData[3], rowData[4]))
    except:
        print("Can't find file at '" + filePath + "'")

    return results

def main():
    print("############################")
    print("#   Auto Work Log v" + appVersion + "   #")
    print("############################")

    today = datetime.today()
    today = datetime(today.year, today.month, today.day, 0, 0, 0) 
    print("\> Date :", today.strftime("%d/%m/%Y"))

    tasks = readTaskSheet(today)

    wl = WorkLog()
    wl.login()
    wl.tasksPage()
    wl.saveTaskDatas(tasks)
    wl.dashboardPage()

    countDownTime = 10
    for i in range(countDownTime):
        print("\> Closing in {0} s".format(countDownTime - i))
        time.sleep(1)

    try:
        wl.close()
    except:
        pass
    exit()

main()
