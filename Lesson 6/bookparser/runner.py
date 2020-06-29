from scrapy.crawler import CrawlerProcess  # Импортируем класс для создания процесса
from scrapy.settings import Settings  # Импортируем класс для настроек

from bookparser import settings  # Наши настройки
from bookparser.spiders.labirint import LabirintSpider  # Класс паука Лабиринт
from bookparser.spiders.book24 import Book24Spider  # Класс паука Book24


if __name__ == '__main__':
    crawler_settings = Settings()  # Создаем объект с настройками
    crawler_settings.setmodule(settings)  # Привязываем к нашим настройкам

    process = CrawlerProcess(settings=crawler_settings)  # Создаем объект процесса для работы
    process.crawl(LabirintSpider)  # Добавляем паука Лабиринт
    process.crawl(Book24Spider)  # Добавляем паука book24

    process.start()  # Пуск
