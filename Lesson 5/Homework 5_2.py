from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')
# Ждем до появления блока Хитов продаж
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "accessories-new")))

# Переходим к блоку Хитов продаж
blocks = driver.find_elements_by_class_name('accessories-new')
actions = ActionChains(driver)
actions.move_to_element(blocks[1])
actions.perform()

exist_element = True
links = []

while exist_element:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sel-hits-button-next")))
    next_button = driver.find_elements_by_class_name('sel-hits-button-next')
    actions = ActionChains(driver)
    actions.move_to_element(next_button[2]).click()
    actions.perform()
    # Проверка достижения конца списка товаров
    try:
        driver.find_element_by_css_selector("a[class='next-btn sel-hits-button-next disabled']")
    # Если не найден элемент конца списка, повторяем цикл
    except NoSuchElementException:
        exist_element = True
    # Найден элемент конца списка, выходим из цикла
    else:
        exist_element = False

# Находим блок Хитов продаж
blocks = driver.find_elements_by_class_name('accessories-new')[1].find_elements_by_class_name('sel-product-tile-title')

link = []

# Перебираем все найденные теги элементов Хитов продаж
for block in blocks:
    item = {}
    # Ссылка на товар
    href = block.get_attribute('href')
    item['link'] = href
    # Наименование товара
    title = block.get_attribute('title')
    item['title'] = title
    # Блок дополнительной информации
    data = block.get_attribute('data-product-info')
    item['data'] = data.replace('\n', '').replace('\t', '')
    links.append(item)

# pprint(links)
client = MongoClient('localhost', 27017)
db = client['my_database']
# Заносим данные в БД my_database в коллекцию mvideo
db.mvideo.insert_many(links)

# Закрываем браузер
driver.quit()
