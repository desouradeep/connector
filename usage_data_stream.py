#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, ctime
from selenium.common.exceptions import NoSuchElementException

import os
import config

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


def authenticate():
    driver.get("http://192.168.0.1")

    username = driver.find_element_by_id("login_n")
    username.send_keys(config.ROUTER_ADMIN_USERNAME)

    password = driver.find_element_by_id("login_pass")
    password.send_keys(config.ROUTER_ADMIN_PASSWORD)

    login = driver.find_element_by_id("Login")
    login.send_keys(Keys.RETURN)
    sleep(1)


driver = create_driver()
authenticate()

while True:
    try:
        usage_dict = {}

        # Get device names from DHCP Client List in router page
        driver.get(config.DHCP_CLIENT_LIST_URL)
        sleep(1)

        client_list_elem = driver.find_element_by_xpath(
            config.CLIENT_LIST_XPATH
        )

        client_list_str = str(client_list_elem.text)
        for client in client_list_str.split("\n")[1:]:
            client_data = client.split()[:3]

            ip = client_data[1]
            usage_dict[ip] = {}
            usage_dict[ip]['name'] = client_data[0]
            usage_dict[ip]['mac'] = client_data[2]

        # Get device usage from Active Sessions page
        driver.get(config.ACTIVE_SESSION_URL)
        sleep(1)

        sessions_list = driver.find_element_by_xpath(
            config.SESSION_XPATH
        )
        sessions_data_str = str(sessions_list.text)
        sessions_data = []
        for session in sessions_data_str.split("\n")[1:]:
            session_data = session.split()
            ip = session_data[0]
            tcp = int(session_data[1])
            udp = int(session_data[2])

            if ip not in usage_dict:
                usage_dict[ip] = {}

            usage_dict[ip]['tcp'] = tcp
            usage_dict[ip]['udp'] = udp

        for i, j in sorted(usage_dict.iteritems()):
            print i + "\t" + str(j)
        print

    except NoSuchElementException:
        authenticate()

    except KeyboardInterrupt:
        print "Ctrl + C pressed. Exiting."
        break
