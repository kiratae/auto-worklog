from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from Helper.selenium import SeleniumHelper
from configSection import ConfigSection
from datetime import datetime
import calendar
import time
import os
import re

class HRM:
    def __init__(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        self.__driver  = webdriver.Chrome(executable_path=os.path.join("Driver", "chromedriver.exe"), options=options)
        self.__config = ConfigSection().hrm
        self.months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
          "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]

    def login(self):
        print("\> HRM:: Loging into app")
        self.__driver.get(self.__config.url)
        assert "Clicknext HRM" in self.__driver.title

        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']//a[contains(@class,'btn-login-google')]"))).click()

        usernameEle = self.__driver.find_element_by_id("identifierId")
        usernameEle.clear()
        usernameEle.send_keys(self.__config.email)
        usernameEle.send_keys(Keys.RETURN)

        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        passwordEle = self.__driver.find_element_by_name("password")
        passwordEle.clear()
        passwordEle.send_keys(self.__config.password)
        passwordEle.send_keys(Keys.RETURN)

        WebDriverWait(self.__driver, 15).until(EC.title_is("[FO] - HRM"))
        print("\> HRM:: Logged in")

    def close(self):
        print("\> HRM:: Closing")
        self.__driver.close()

    def timeSheetListPage(self, date = None, isOnlyDraft = True):
        print("\> HRM:: Goto time-sheet list page")
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='aside_menu']//*[@id='menu_FN-TAT-10']/a"))).click()

        if date == None:
            date = datetime.today()
        
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#select2-Month-container"))).click()
        select2Ele = self.__driver.find_element_by_css_selector("input.select2-search__field")
        select2Ele.clear()
        select2Ele.send_keys(self.months[date.month - 1])
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-results__option--highlighted"))).click()

        if isOnlyDraft:
            WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@aria-labelledby, 'select2-TimesheetStatusId-container')]"))).click()
            WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='select2-TimesheetStatusId-results']//*[text()='บันทึกร่าง']"))).click()

        self.__driver.find_element_by_id("form-search").submit()

    def timeSheetEditPage(self, date = None):
        print("\> HRM:: Goto time-sheet edit page")

        if date == None:
            date = datetime.today()

        matchMonthYearEle = None
        html_list = self.__driver.find_element_by_css_selector("table.datatable__table tbody")
        items = html_list.find_elements_by_tag_name("tr")
        for item in items:
            year = item.find_element_by_xpath("//td[3]").text
            month = item.find_element_by_xpath("//td[4]").text
            if int(year) == date.year + 543 and month == self.months[date.month - 1]:
                matchMonthYearEle = item.find_element_by_xpath("//td[6]/a")

        if matchMonthYearEle != None:
            matchMonthYearEle.click()
        else:
            WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']//a[contains(@class, 'do-add')]"))).click()

    def addProjectRow(self, row, project, datas, isCretedNew = False, date = None):
        print("\> HRM:: Adding new project record", project)
        if isCretedNew:
            WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.ID, "btn-add-project"))).click()
        
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//tr[@id='row_timesheetRec_{0}']//*[contains(@class,'select2-container')]".format(row+1)))).click()
        select2Ele = self.__driver.find_element_by_css_selector("input.select2-search__field")
        select2Ele.clear()
        select2Ele.send_keys(project)
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-results__option--highlighted"))).click()

        if date == None:
            date = datetime.today()

        daysInMonth = calendar.monthrange(date.year, date.month)[1]
        for day in range(1, daysInMonth):
            daySelector = "#row_timesheetRec_{0} input[name='TimesheetRecs[{1}].D{2}Text']".format(row+1, row, day)
            dayEle = self.__driver.find_element_by_css_selector(daySelector)
            dayEle.clear()
            time.sleep(0.2)
            timeSpentInHour = datas[datetime(date.year, date.month, day)]
            if timeSpentInHour != 0:
                dayEle.send_keys(timeSpentInHour)

    def saveDraftTimeSheet(self):
        print("\> HRM:: Saving-draft time sheet")
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
            (By.ID, "btn-draft"))).click()
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".swal2-popup .swal2-confirm"))).click()
