from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from Helper.selenium import SeleniumHelper
from configSection import ConfigSection
from Class.task import Task
from datetime import datetime
import os
import re

class WorkLog:
    def __init__(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--disable-extensions")
        self.__driver  = webdriver.Chrome(executable_path=os.path.join("Driver", "chromedriver.exe"), options=options)
        self.__config = ConfigSection().worklog

    def login(self):
        print("\> WorkLog:: Loging into app")
        self.__driver.get(self.__config.url)
        assert "Task" in self.__driver.title
        usernameEle = self.__driver.find_element_by_name("userName")
        usernameEle.clear()
        usernameEle.send_keys(self.__config.username)
        passwordEle = self.__driver.find_element_by_name("password")
        passwordEle.clear()
        passwordEle.send_keys(self.__config.password)
        self.__driver.find_element_by_id("main").submit()

    def close(self):
        print("\> WorkLog:: Closing")
        self.__driver.close()

    def tasksPage(self):
        print("\> WorkLog:: Goto task list page")
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='sidebarnav']/*/a[@href='/wa/task/worklog/list']"))).click()

    def timelinePage(self, date = None, onlyMe = True):
        print("\> WorkLog:: Goto timeline page")
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='sidebarnav']/*/a[@href='/wa/task/report/timeline']"))).click()

        if date == None:
            date = datetime.today()

        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@id='Year']/option[@value='{0}']".format(date.year)))).click()

        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@id='Month']/option[@value='{0}']".format(date.month)))).click()

        if onlyMe:
            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//select[@id='EmployeeId']/option[starts-with(text(),'{0}')]".format(self.__config.name)))).click()

        results = []
        html_list = self.__driver.find_element_by_css_selector("ul.timeline")
        items = html_list.find_elements_by_tag_name("li")
        index = 0
        for item in items:
            index += 1
            print("\> WorkLog:: Reading task [{0}/{1}]".format(index, len(items)))
            name = item.find_element_by_css_selector(".timeline-heading .timeline-title").text
            try:
                desc = item.find_element_by_css_selector(".timeline-body div").text
            except:
                desc = None
            dateText = item.find_element_by_css_selector(".timeline-heading div span.text-muted").text
            date = re.findall("(\d{2})\/(\d{2})\/(\d{4})", dateText)[0]
            date = datetime(int(date[2]) - 543, int(date[1]), int(date[0]))
            timeSpentText = item.find_element_by_css_selector(".timeline-heading div small.text-muted").text
            timeSpent = re.findall("(\d+)", timeSpentText)[0]
            try:
                project = item.find_element_by_css_selector(".timeline-heading div span.badge").text
            except:
                project = None
            results.append(Task(date, project, timeSpent, name, desc))
        
        return results

    def dashboardPage(self):
        print("\> WorkLog:: Goto dashboard page")
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='sidebarnav']/*/a[@href='/wa/task/report/rpt01']"))).click()

    def createTaskPage(self):
        print("\> WorkLog:: Goto task edit page")
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='main-wrapper']//a[@href='/wa/task/worklog/edit']"))).click()

    def saveTaskData(self, task: Task):
        print("\> WorkLog:: Saving task \"{0}\"".format(task.toString()))

        if task.project != None and task.project != "":
            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2"))).click()
            select2Ele = self.__driver.find_element_by_css_selector(
                "input.select2-search__field")
            select2Ele.clear()
            select2Ele.send_keys(task.project)

            WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".select2-results__option--highlighted"))).click()

        timeSpentEle = self.__driver.find_element_by_id("TimeSpent")
        timeSpentEle.clear()
        timeSpentEle.send_keys(task.timeSpent)

        nameEle = self.__driver.find_element_by_id("Name")
        nameEle.clear()
        nameEle.send_keys(task.name)

        descEle = self.__driver.find_element_by_id("Description")
        descEle.clear()
        descEle.send_keys(task.desc)

        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn-save"))).click()
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".swal2-popup .swal2-confirm"))).click()

    def saveTaskDatas(self, tasks):
        print("\> WorkLog:: Saving {0} task{1}".format(len(tasks), "" if len(tasks) == 1 else "s"))
        for i in range(len(tasks)):
            print("\> WorkLog:: Saving [{0}/{1}]".format(i+1, len(tasks)))
            self.createTaskPage()
            self.saveTaskData(tasks[i])
        print("\> WorkLog:: {0} task{1} are saved".format(len(tasks), "" if len(tasks) == 1 else "s"))
