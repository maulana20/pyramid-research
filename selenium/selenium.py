from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

driver = webdriver.Chrome()
driver.get("http://localhost/login/")
assert "Login" in driver.title
elem = driver.find_element_by_xpath("//input[@placeholder='Username']").send_keys("maulana_versatech")
elem = driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Csatversa123")
elem = driver.find_element_by_xpath("//button[contains(text(), 'Login')]").click()

time.sleep(10)
assert "No results found." not in driver.page_source
driver.close()
