from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

import logging

driver = webdriver.Chrome()
driver.get("http://localhost/login/")
assert "Login" in driver.title
elem = driver.find_element_by_xpath("//input[@placeholder='Username']").send_keys("maulana_versatech")
elem = driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Csatversa123")
elem = driver.find_element_by_xpath("//button[contains(text(), 'Login')]").click()

time.sleep(10)

elem = driver.find_element_by_xpath("//span/a[@title='Collapse Menu']").click()
time.sleep(5)

elem = driver.find_element_by_xpath("//span/a[@title='Collapse Menu']").click()
time.sleep(5)

elem = driver.find_element_by_id("logout").click()

time.sleep(5)

#assert "No results found." not in driver.page_source
driver.close()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#Create a file handler
handler_warn = logging.FileHandler('warning_log.txt')
handler_warn.setLevel(logging.WARNING)

handler_info = logging.FileHandler('info_log.txt')
handler_info.setLevel(logging.INFO)

#create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler_warn.setFormatter(formatter)
handler_info.setFormatter(formatter)


#add the handler to the logger

logger.addHandler(handler_warn)
logger.addHandler(handler_info)


logger.info(elem)
logger.warning(elem)
