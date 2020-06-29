import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.catalog-pagination__item._text::attr(href)').extract()[-1]

        # Получаем ссылки на книги каждой страницы next_page
        book_links = response.css('div.book__image-block a::attr(href)').extract()

        # Обход каждой книги
        for book in book_links:
            yield response.follow(book, callback=self.book_parse)

        # Переход на следующую страницу
        yield response.follow(next_page, callback=self.parse)

    # Парсинг параметров
    def book_parse(self, response: HtmlResponse):
        link_book = response.xpath("//meta[@property='og:url']/@content").extract_first()
        name_book = response.xpath('//h1/text()').extract_first()
        author_book = response.xpath('//div[@class="item-tab__chars-item"][1]//a//text()').extract()
        main_price_book = response.xpath('//div[@class="item-actions__price-old"]/text()').extract_first()
        sale_price_book = response.xpath('//div[@class="item-actions__price"]/b/text()').extract_first()
        rating_book = response.xpath('//span[@class="rating__rate-value"]/text()').extract_first()

        # Передача параметров в items
        yield BookparserItem(link=link_book, name=name_book, author=author_book, main_price=main_price_book,
                             sale_price=sale_price_book, rating=rating_book)

