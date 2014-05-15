#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, ctime
from sys import stdout
from selenium.common.exceptions import WebDriverException
import os
import config

SLEEP_TIME = 10 * 60  # 10 minutes

DEFAULT_COLOR = '\033[0m'
NOTIFY_COLOR = '\033[93m'
TIMER_COLOR = '\033[94m'


def log(sentence):
    print "%s%s:%s %s" % (NOTIFY_COLOR, ctime(), DEFAULT_COLOR, sentence)


def create_driver():
    log("Creating webdriver")
    chromedriver_filename = 'chromedriver'
    CHROME_DRIVER = os.path.join(os.getcwd(), chromedriver_filename)
    driver = webdriver.Chrome(CHROME_DRIVER)
    #phantomjs_filename = 'phantomjs'
    #phantomjs_location = os.path.join(os.getcwd(), phantomjs_filename)
    #driver = webdriver.PhantomJS(phantomjs_location)
    return driver


def connect():
    try:
        driver = create_driver()
    except WebDriverException:
        log("Exception occurred while creating webdriver")
        return

    USERNAME = config.USERNAME
    PASSWORD = config.PASSWORD

    LOGIN_URL = config.LOGIN_URL

    log("Connecting to login server")
    try:
        driver.get(LOGIN_URL)
    except Exception:
        log("Couldn't fetch login page")
        return

    try:
        assert '24Online Client' in driver.title
        log("Connection successful")
    except Exception:
        log("Connection failed")
        driver.quit()
        return

    username_xpath = config.USERNAME_XPATH

    password_xpath = config.PASSWORD_XPATH

    submit_xpath = config.SUBMIT_XPATH

    try:
        username_elem = driver.find_element_by_xpath(username_xpath)
        password_elem = driver.find_element_by_xpath(password_xpath)
        submit_elem = driver.find_element_by_xpath(submit_xpath)
    except Exception:
        log("Couldn't find elements by xpath")
        return

    log("Filling login credentials")

    try:
        username_elem.send_keys(USERNAME)
        password_elem.send_keys(PASSWORD)
        log("Authenticating")
        submit_elem.send_keys(Keys.RETURN)
    except Exception:
        log("Couldn't send authentcation keys")
        return

    sleep(2)
    log("Quiting webdriver")
    driver.quit()

log("Program Started")
establish_connection = True

trial = 0
while establish_connection:
    try:
        log("Attempting to connect...")
        connect()
        print
        trial += 1
        for i in range(SLEEP_TIME, -1, -1):
            stdout.write(
                "\r%s%s: %s[TRIAL %d] Reconnecting in:%s %ds " %
                (NOTIFY_COLOR, ctime(), TIMER_COLOR, trial, DEFAULT_COLOR, i)
            )
            stdout.flush()
            if i != 0:
                sleep(1)
        print "\n"
    except KeyboardInterrupt:
        establish_connection = False
        print "\nCtrl+C Pressed. Exiting."
