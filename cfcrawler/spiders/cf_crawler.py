# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from cfcrawler.items import CoreHTML
from scrapy.utils.python import to_native_str


class CFSpider(CrawlSpider):

    # Handle Error Codes selbst
    handle_httpstatus_list = [301, 302, 404]

    # Domain Input  
    try:
        global name_domain
        name_domain = input("Domain eingeben: ")
    except:
        pass

    # Build URLs
    http_domain = "http://" + name_domain
    http_wwwdomain = "http://www." + name_domain
    https_domain = "https://" + name_domain
    https_wwwdomain = "https://www." + name_domain

    # Crawler Start
    name = 'cf-crawler'
    allowed_domains = [name_domain]
    start_urls = [https_domain, https_wwwdomain, http_domain, http_wwwdomain]
    
    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )
    
    # Spezielle Settings
    custom_settings = {
        
    # Reihenfolge in dem die Felder exportiert werden
    'FEED_EXPORT_FIELDS': ["url", "status_code", "cache_control", "title", "title_length", "title_count", "description", "description_length",  "description_count", "canonical", "canonical_self", "h1", "h1_count", "wordcount", "internal_links", "external_links", "amp_html", "amp_valid", "redirect_location", "referrer"],
        
     }
    
    def parse_item(self, response):
        
        if response.status == 200:
            
            # 200 EXTRACTION DEFINITION
            # URL Info
            url = response.url
            status_code = response.status
            internal_links = []
            external_links = []

            # HTTP Header
            cache_control = response.headers.get('Cache-control')
            referrer = to_native_str(response.request.headers.get('Referer', None))

            # AMP
            amp_html = response.xpath("//link[@rel='amphtml']/@href").extract_first()
            amp_valid = ""

            # Tracking
            #gtm_check = scrapy.Field()

            # Main HTML Tags
            #meta_robots = scrapy.Field()
            title = response.css('title::text').extract_first()
            title_length = "0"
            title_count = "0"
            description = response.xpath('//meta[@name="description"]/@content').extract_first()
            description_length = "0"
            description_count = "0"
            h1 = response.xpath('//h1/text()').extract_first()
            h1_count = "0"
            canonical = response.xpath('//link[@rel="canonical"]/@href').extract_first()
            #canonical_self = scrapy.Field()
            #wordcount = scrapy.Field()

            # Social Tags
            #og_title = scrapy.Field()
            #og_description = scrapy.Field()
            #og_image = scrapy.Field()
            #twitter_title = scrapy.Field()
            #twitter_description = scrapy.Field()
            #twitter_image = scrapy.Field()

            # CFCD Tags
            #cf_maintag = scrapy.Field()
            #cf_articletype = scrapy.Field()
            
            # Canoncial Check
            if url == canonical:
                canonical_check = True
            else:
                canonical_check = False
            
            # AMP Validation    
            try:
                amp_valid = requests.get('https://amp.cloudflare.com/q/' + amp_html.replace("https://", "")).json()["valid"]
            except:
                pass
            
            # Strip Check (If it exists, strip it, so get rid of /n
            if not title is None:
                title = title.strip()
                title_length = len(title)
                title_count = len(response.css('title::text').extract())
                
            if not description is None:
                description = "".join(description.splitlines())
                description_length = len(description)
                description_count = len(response.xpath('//meta[@name="description"]/@content').extract())

            # H1 Check -> Unterschiedliche Implementierung
            if h1 is None:
                h1 = response.xpath('//h1/*/text()').extract_first()    
                if not h1 is None:
                    h1 = h1.strip()
                    h1_count = len(response.xpath('//h1/*/text()').extract())
            else:
                h1 = h1.strip()
                h1_count = len(response.xpath('//h1/text()').extract())
            
            if not cache_control is None:
                cache_control = to_native_str(cache_control.decode('latin1'))
                
            # Counting Links

            for link in LinkExtractor(allow=(self.allowed_domains)).extract_links(response):
                internal_links.append(link.url)

            for link in LinkExtractor(allow=(),deny = self.allowed_domains).extract_links(response):
                external_links.append(link.url)
                
            
            # Export
            yield {
                'url': url,
                'status_code': status_code,
                'cache_control': cache_control,
                'title': title,
                'title_length': title_length,
                'title_count': title_count,
                'description': description,
                'description_length': description_length,
                'description_count': description_count,
                'canonical': canonical,
                'canonical_self': canonical_check,
                'h1': h1,
                'h1_count': h1_count,
                'internal_links' : len(internal_links),
                'external_links' : len(external_links),
                'amp_html': amp_html,
                'amp_valid': amp_valid,
                'referrer': referrer
            }
        
        elif response.status in [301, 302]:
            
            # 300 EXTRACTION DEFINITION
            # URL Info
            url = response.url
            status_code = response.status

            # HTTP Header
            cache_control = response.headers.get('Cache-control')
            redirect_location = to_native_str(response.headers.get('Location').decode('latin1'))
            referrer = to_native_str(response.request.headers.get('Referer', None))
            
            # Strip Check (If it exists, strip it, so get rid of /n
            if not cache_control is None:
                cache_control = to_native_str(cache_control.decode('latin1'))
            
            # EXPORT
            yield {
                'url': url,
                'status_code': status_code,
                'cache_control': cache_control,
                'redirect_location': redirect_location,
                'referrer': referrer
            }
            
            # Submit Redirect Location to Queue
            yield scrapy.Request(url = redirect_location, callback=self.parse_item)
            
        
        elif response.status >= 400:
            
            # ERROR EXTRACTION DEFINITION
            # URL Info
            url = response.url
            status_code = response.status

            # HTTP Header
            cache_control = cache_control = response.headers.get('Cache-control')
            referrer = to_native_str(response.request.headers.get('Referer', None))  
            
            # Strip Check (If it exists, strip it, so get rid of /n
            if not cache_control is None:
                cache_control = to_native_str(cache_control.decode('latin1'))
            
            # EXPORT
            yield {
                'url': url,
                'status_code': status_code,
                'cache_control': cache_control,
                'referrer': referrer
            }
