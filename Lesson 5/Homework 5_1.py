from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


driver = webdriver.Chrome()

driver.get('https://mail.ru')
time.sleep(1)
assert "Mail" in driver.title

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_id("mailbox:submit").click()

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NextPassword172')

elem.send_keys(Keys.RETURN)

