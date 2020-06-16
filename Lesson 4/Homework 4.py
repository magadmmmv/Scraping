from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

# Блок спортивных новостей https://yandex.ru/news
response = requests.get('https://yandex.ru/news', headers=header)

dom = html.fromstring(response.text)

blocks = dom.xpath("//div[@class='stories-set stories-set_main_no stories-set_pos_7']//tr/td")

links = []
for block in blocks:
    item = {}
    name = block.xpath(".//div//h2//a/text()")
    a = block.xpath(".//div//h2//a/@href")
    datetime = block.xpath(".//div[@class='story__date']/text()")
    item['name'] = name[0]
    item['url'] = 'https://yandex.ru' + str(a[0])
    item['datetime'] = datetime[0]
    item['source'] = datetime[0]
    links.append(item)


# Блок новостей lenta.ru в центральной области
response = requests.get('https://lenta.ru', headers=header)

dom = html.fromstring(response.text)

blocks = dom.xpath("//section[contains(@class, 'js-top-seven')]/div[@class]/div[not(contains(@class,'button-more-news'))][contains(@class, 'first-item')]/h2/a | //section[contains(@class, 'js-top-seven')]/div[@class]/div[not(contains(@class,'button-more-news'))][not(contains(@class, 'first-item'))]/a")

for block in blocks:
    item = {}
    name = block.xpath("./text()")
    a = block.xpath("./@href")
    datetime = block.xpath("./time/@datetime")
    item['name'] = name[0]
    item['url'] = 'https://lenta.ru' + str(a[0])
    item['datetime'] = datetime[0]
    item['source'] = 'https://lenta.ru'
    links.append(item)

# pprint(links)
client = MongoClient('localhost', 27017)
db = client['my_database']
db.news.insert_many(links)
