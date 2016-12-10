# -*- coding: utf-8 -*-
import scrapy
from proxylist.items import ScrapyTestItem

class ProxyListSpider(scrapy.Spider):
    name = "proxylist"
    allowed_domains = ["free-proxy-list.net"]
    start_urls = [
        "https://free-proxy-list.net/",
    ]
    
    def parse(self, response):
        trs = response.css('tbody tr')
        for tr in trs:
            item = ScrapyTestItem()
            tds = tr.css('td')
            item['ip'] = tds[0].xpath('text()').extract()[0]
            item['port'] = tds[1].xpath('text()').extract()[0]
            yield item


class KuaidailiSpider(scrapy.Spider):
    name = "kuaidaili"
    allowed_domains = ["kuaidaili.com"]
    start_urls = [
        "http://www.kuaidaili.com/proxylist/1/",
    ]

    def parse(self, response):
        trs = response.css('tbody tr')
        for tr in trs:
            item = ScrapyTestItem()
            tds = tr.css('td')
            item['ip'] = tds[0].xpath('text()').extract()[0]
            item['port'] = tds[1].xpath('text()').extract()[0]
            yield item
        for a in response.css('#listnav ul li a::attr(href)').extract():
            if not a:
                continue
            next_page = response.urljoin(a)
            yield scrapy.Request(next_page, callback=self.parse)


class XroxySpider(scrapy.Spider):
    name = "xroxy"
    allowed_domains = ["xroxy.com"]
    start_urls = [
        "http://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&sort=reliability&desc=true&pnum=0#table",
    ]

    def parse(self, response):
        ips = [x.strip() for x in response.xpath('//a[@title="View this Proxy details"]/text()').extract() if x != '\n']
        ports = [x.strip() for x in response.xpath('//a[contains(@title,"Select proxies with port number")]/text()').extract() if x != '\n']
        if len(ips) == len(ports):
            for x in range(0, len(ips)):
                item = ScrapyTestItem()
                item['ip'] = ips[x]
                item['port'] = ports[x]
                yield item

        for a in response.xpath('//small/a/@href').extract():
            if not a:
                continue
            next_page = response.urljoin(a)
            yield scrapy.Request(next_page, callback=self.parse)
