# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):  # Конструктор, где инициализируем подключение к СУБД
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.book_scrapy

    def process_item(self, item, spider):
        # Обработка параметров сайта Лабиринт
        if spider.name == 'labirint':
            item['author'] = ' '.join(item['author'][1:])
            item['main_price'] = int(item['main_price'])
            item['sale_price'] = int(item['sale_price'])
            item['rating'] = float(item['rating'])
        # Обработка параметров сайта Book24
        elif spider.name == 'book24':
            item['author'] = ' '.join(item['author'])
            item['sale_price'] = int(item['sale_price'].replace(' ', ''))

            if item['main_price'] is None:
                item['main_price'] = item['sale_price']
            else:
                item['main_price'] = int(' '.join(item['main_price'].split(' '))[:-3].replace(' ', ''))

            if item['rating'] is None:
                item['rating'] = 0.0
            else:
                item['rating'] = float(item['rating'].replace(',', '.'))

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
