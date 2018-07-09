# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class CoreHTML(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # URL Info
    url = scrapy.Field()
    status_code = scrapy.Field()
    internal_links = scrapy.Field()
    external_links = scrapy.Field()
    
    # HTTP Header
    cache_control = scrapy.Field()
    redirect_location = scrapy.Field()
    referrer = scrapy.Field()
    
    # AMP
    amp_html = scrapy.Field()
    amp_valid = scrapy.Field()
    
    # Tracking
    gtm_check = scrapy.Field()
    
    # Main HTML Tags
    meta_robots = scrapy.Field()
    title = scrapy.Field()
    title_length = scrapy.Field()
    title_count = scrapy.Field()
    description = scrapy.Field()
    description_length = scrapy.Field()
    description_count = scrapy.Field()
    h1 = scrapy.Field()
    h1_count = scrapy.Field()
    canonical = scrapy.Field()
    canonical_self = scrapy.Field()
    wordcount = scrapy.Field()
    
    # Social Tags
    og_title = scrapy.Field()
    og_description = scrapy.Field()
    og_image = scrapy.Field()
    twitter_title = scrapy.Field()
    twitter_description = scrapy.Field()
    twitter_image = scrapy.Field()
    
    # CFCD Tags
    cf_maintag = scrapy.Field()
    cf_articletype = scrapy.Field()
    
    