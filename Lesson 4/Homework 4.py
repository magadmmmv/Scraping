from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
from datetime import date
from datetime import datetime
import locale


# Функция перевода даты в именительный падеж
def ru_month_format(ru_month):
    ru_month_values = {
        'января': 'январь',
        'февраля': 'февраль',
        'марта': 'март',
        'апреля': 'апрель',
        'мая': 'май',
        'июня': 'июнь',
        'июля': 'июль',
        'августа': 'август',
        'сентября': 'сентябрь',
        'октября': 'октябрь',
        'ноября': 'ноябрь',
        'декабря': 'декабрь',
    }
    return ru_month_values[ru_month]


header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97'
}

links = []

# Перевод наименования месяца в кириллицу
locale.setlocale(locale.LC_ALL, 'RU')
current_date = date.today().strftime("%d %B %Y")

# Блок спортивных новостей https://yandex.ru/news
response = requests.get('https://yandex.ru/news', headers=header)
dom = html.fromstring(response.text)
blocks = dom.xpath("//div[@class='stories-set stories-set_main_no stories-set_pos_7']//tr/td")

for block in blocks:
    item = {}
    name = block.xpath(".//h2[@class='story__title']//text()")
    a = block.xpath(".//h2[@class='story__title']//@href")
    date_time = block.xpath(".//div[@class='story__date']/text()")
    item['name'] = name[0]
    item['url'] = 'https://yandex.ru' + str(a[0])
    # Преобразование даты требуемого формата в текст
    str_date = date_time[0].replace('\xa0', ' ').replace('в ', '').split()[-1] + ', ' + str(current_date)
    # Преобразование текста в datetime
    to_date = datetime.strptime(str_date, '%H:%M, %d %B %Y')
    # Записываем дату в общем формате
    item['datetime'] = to_date.strftime('%H:%M, %d %B %Y')
    item['source'] = ' '.join(date_time[0].replace('\xa0', ' ').replace('в ', '').split()[:-1])
    links.append(item)

# Блок новостей lenta.ru в центральной области
response = requests.get('https://lenta.ru', headers=header)
dom = html.fromstring(response.text)
path = "//section[contains(@class, 'js-top-seven')]/div[@class]/div[not(contains(@class,'button-more-news'))]" \
       + "[contains(@class, 'first-item')]/h2/a " \
       + "| //section[contains(@class, 'js-top-seven')]/div[@class]/div[not(contains(@class,'button-more-news'))]" \
       + "[not(contains(@class, 'first-item'))]/a"
blocks = dom.xpath(path)

for block in blocks:
    item = {}
    name = block.xpath("./text()")
    a = block.xpath("./@href")
    date_time = block.xpath("./time/@datetime")
    item['name'] = name[0].replace('\xa0', ' ')
    item['url'] = 'https://lenta.ru' + str(a[0])
    # Получаем название месяца для дальнейшего перевода в именительный падеж
    month = date_time[0].split()[-2]
    # Преобразование текста в datetime
    to_date = datetime.strptime(date_time[0][1:].replace(month, ru_month_format(month)), '%H:%M, %d %B %Y')
    # Записываем дату в общем формате
    item['datetime'] = to_date.strftime('%H:%M, %d %B %Y')
    item['source'] = 'https://lenta.ru'
    links.append(item)

# Блок первых новостей news.mail.ru
response = requests.get('https://news.mail.ru', headers=header)
dom = html.fromstring(response.text)
blocks = dom.xpath('//ul[@data-module="TrackBlocks"]//a[@class="list__text"]')

for block in blocks:
    item = {}
    name = block.xpath("./text()")
    a = block.xpath("./@href")
    item['name'] = name[0].replace('\xa0', ' ')
    # Разделяем внешние и внутренние ссылки
    if str(a[0])[0] == '/':
        item['url'] = 'https://news.mail.ru' + str(a[0])
    else:
        item['url'] = str(a[0])

    # Заходим по ссылке новости для извлечения даты публикации и источника
    response_block = requests.get(item['url'], headers=header)
    dom_block = html.fromstring(response_block.text)
    blocks_block = dom_block.xpath('//span[@class="breadcrumbs__item"]/span')

    date_time = blocks_block[0].xpath('./span/@datetime')
    source = blocks_block[1].xpath('.//span[@class="link__text"]/text()')
    # Преобразование текста в datetime
    to_date = datetime.strptime(date_time[0].replace('T', ' ')[:15], '%Y-%m-%d %H:%M')
    # Записываем дату в общем формате
    item['datetime'] = to_date.strftime('%H:%M, %d %B %Y')
    item['source'] = source[0]
    links.append(item)

# pprint(links)
client = MongoClient('localhost', 27017)
db = client['my_database']
# Заносим данные в БД my_database в коллекцию news
db.news.insert_many(links)
