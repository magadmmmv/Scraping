import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/']

    def parse(self, response: HtmlResponse):
        next_page = response.css('div.pagination-number-viewport a.pagination-next__text::attr(href)').extract_first()

        # Получаем ссылки на книги каждой страницы next_page
        book_links = response.css('a.product-title-link::attr(href)').extract()

        # Обход каждой книги
        for book in book_links:
            yield response.follow(book, callback=self.book_parse)

        # Переход на следующую страницу
        yield response.follow(next_page, callback=self.parse)

    # Парсинг параметров
    def book_parse(self, response: HtmlResponse):
        link_book = response.xpath("//meta[@property='og:url']/@content").extract_first()
        name_book = response.xpath('//h1/text()').extract_first()
        author_book = response.xpath('//div[@class="authors"][1]//text()').extract()
        main_price_book = response.xpath('//span[@class="buying-priceold-val-number"]/text()').extract_first()
        sale_price_book = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').extract_first()
        rating_book = response.xpath('//div[@id="rate"]/text()').extract_first()

        # Передача параметров в items
        yield BookparserItem(link=link_book, name=name_book, author=author_book, main_price=main_price_book,
                             sale_price=sale_price_book, rating=rating_book)




