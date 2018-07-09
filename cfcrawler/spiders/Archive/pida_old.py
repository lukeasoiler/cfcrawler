# -*- coding: utf-8 -*-
import scrapy
#import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from cfcrawler.items import CoreHTML

class PidaSpider(CrawlSpider):
    name = 'pida_old'
    allowed_domains = ['pille-danach.de']
    start_urls = ['https://pille-danach.de']
    handle_httpstatus_all = True
    rules = (Rule(LinkExtractor(allow=()), callback='parse_obj', follow=True),)
    
    # Spezielle Settings
    custom_settings = {
        
    # Reihenfolge in dem die Felder exportiert werden
    'FEED_EXPORT_FIELDS': ["url", "status_code", "cache_control", "title", "title_length", "description", "description_length",  "canonical", "canonical_self", "h1", "wordcount", "internal_links", "external_links", "amp_html", "amp_valid"],
        
     }
    
    def parse_obj(self,response):
        
        if response.status == 200:
        
            # Definition der Extractions
            url = response.url
            status_code = response.status
            cache_control = response.headers['cache-control']
            title = response.css('title::text').extract_first()
            description = response.xpath('//meta[@name="description"]/@content').extract_first()
            canonical = response.xpath('//link[@rel="canonical"]/@href').extract_first()
            h1 = response.css('h1::text').extract_first()
            articlebody = response.xpath('//div[@itemprop="articleBody"]/*[not(script)]//text()').extract()
            amp_html = response.xpath("//link[@rel='amphtml']/@href").extract_first()


            # Canonical Check
            if url == canonical:
                canonical_check = "OK" 
            else: 
                canonical_check = "FALSE"

            # AMP Validation
            #try:
            #    amp_valid = requests.get('https://amp.cloudflare.com/q/' + amp_html.replace("https://", "")).json()["valid"]
            #except:
            #    pass

            # Article Extracting
            articlebody = ''.join(articlebody).replace('.',' ').replace('?',' ').replace(",",' ').replace("-",' ').replace("!",' ').lower().split(' ')
            articlebody = [(elelemt.strip()) for elelemt in articlebody]
            articlebody = list(filter(None, articlebody))

            # Counting Links
            internal_links = []
            external_links = []

            for link in LinkExtractor(allow=(self.allowed_domains)).extract_links(response):
                internal_links.append(link.url)

            for link in LinkExtractor(allow=(),deny = self.allowed_domains).extract_links(response):
                external_links.append(link.url)

            # Extract to Item
            item = CoreHTML()
            item["url"] = url
            item["status_code"] = status_code
            item["cache_control"] = cache_control
            item["title"] = title
            item["title_length"] = len(title)
            item["description"] = description
            item["description_length"] = len(description)
            item["canonical"] = canonical
            item["canonical_self"] = canonical_check
            item["h1"] = h1
            item["wordcount"] = len(articlebody)
            item["internal_links"] = len(internal_links)
            item["external_links"] = len(external_links)
            item["amp_html"] = amp_html
            #item["amp_valid"] = amp_valid

            return item
        
        else:
            
            item = CoreHTML()
            item["url"] = url
            item["status_code"] = status_code

            return item
            
    
    
    
    