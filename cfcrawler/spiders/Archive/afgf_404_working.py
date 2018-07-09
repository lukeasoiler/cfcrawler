# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from cfcrawler.items import CoreHTML


class PidaSpider(CrawlSpider):
    handle_httpstatus_list = [404]
    name = 'afgf_404_working'
    allowed_domains = ['friends.aok.de']
    start_urls = ['http://friends.aok.de']
    
    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )
    
    # Spezielle Settings
    custom_settings = {
        
    # Reihenfolge in dem die Felder exportiert werden
    'FEED_EXPORT_FIELDS': ["url", "status_code", "cache_control", "title", "title_length", "description", "description_length",  "canonical", "canonical_self", "h1", "wordcount", "internal_links", "external_links", "amp_html", "amp_valid"],
        
     }

    def parse_item(self, response):
        
        item = CoreHTML()
        
        if response.status == 200:
            item["url"] = response.url
            item["status_code"] = response.status

            return item
        
        elif response.status == 404:
            item["url"] = response.url
            item["status_code"] = response.status

            return item
