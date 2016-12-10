# -*- coding: utf-8 -*-
import scrapy
from dahai.items import DahaiItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["dhzw.com"]
    start_urls = ['http://www.dhzw.com/']

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_page,
                                 errback=self.errback)

    def parse_page(self, response):
        yield self.pasrse_item(response)
        for a in response.css('a::attr(href)').extract():
            if not a:
                continue
            next_page = response.urljoin(a)
            #print next_page
            yield scrapy.Request(next_page, callback=self.parse_page)

    def pasrse_item(self, response):
        booktext = response.css('#BookText::text').extract()
        if len(booktext) != 0:
            title = response.css('title::text').extract()[0]
            item = DahaiItem()
            item['booktext'] = booktext
            item['title'] = title
            return item
        return None

    def errback(self, faulure):
        pass