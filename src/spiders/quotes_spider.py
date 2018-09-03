import scrapy
from functools import reduce


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://citaty.info/category/zhiznennye-citaty',
    ]

    def parse(self, response):
        for quote in response.css('div.view-content div.quotes-row'):
            yield {
                'text': reduce((lambda x, y: '%s %s' % (x, y)), quote.xpath('.//p//text()').extract()).replace('\xa0', ' ').replace('  ', ' '),
                'sources': quote.xpath(".//div[contains(@class, 'node__content')]/div[contains(@class, 'field-type-taxonomy-term-reference')]//text()").extract(),
                'tags': quote.xpath(".//div[contains(@class, 'node__topics')]//div[contains(@class, 'field-item')]//text()").extract()
            }

        next_page = response.css('li.pager-next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)