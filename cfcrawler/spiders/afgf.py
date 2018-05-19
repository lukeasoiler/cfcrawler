# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AfgfSpider(CrawlSpider):
    name = 'afgf'
    allowed_domains = ['friends.aok.de']
    start_urls = ['http://friends.aok.de/']

    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        i['name'] = response.status
        i['url'] = response.url
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
