from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
from pprint import pprint

driver = webdriver.Chrome()

# Авторизация
driver.get('https://m.mail.ru/login')
time.sleep(1)
assert "Mail" in driver.title

elem = driver.find_element_by_name('Login')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_name('Password')
elem.send_keys('NextPassword172')

elem.send_keys(Keys.RETURN)

# Ищем и переходим в первое письмо
link = driver.find_element_by_class_name('messageline__link')
driver.get(link.get_attribute('href'))

# Первое письмо последней вкладки для быстрой проверки
# test_letter = 'https://m.mail.ru/message/15629228431794183842'
# driver.get(test_letter)

exist_element = True
links = []

while exist_element:
    try:
        item = {}
        date = driver.find_element_by_class_name('readmsg__mail-date')
        item['date'] = date.text
        sender = driver.find_element_by_class_name('readmsg__text-container__inner-line').find_element_by_tag_name('strong')
        item['sender'] = sender.text
        title = driver.find_element_by_class_name('readmsg__theme')
        item['title'] = title.text
        body = driver.find_element_by_id('readmsg__body')
        item['body'] = body.text.replace('\n', ' ').replace('\u200c', '')
        links.append(item)
        # Переходим по кнопке "Следующее" на очередное письмо
        next_page = driver.find_element_by_link_text('Следующее')
        driver.get(next_page.get_attribute('href'))
    # Если кнопка "Следующее" не найдено, то выходим из цикла
    except NoSuchElementException:
        exist_element = False

# pprint(links)

client = MongoClient('localhost', 27017)
db = client['my_database']
# Заносим данные в БД my_database в коллекцию mail
db.mail.insert_many(links)

# Закрываем браузер
driver.quit()
