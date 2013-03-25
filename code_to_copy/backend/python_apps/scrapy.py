#!/usr/bin/env python
#-*- coding:utf8 -*-

# 在shell下玩scrapy
scrapy shell http://XXX.XXX
scrapy crawl --output XXX_FILE --nolog   XXXspider


# 写爬虫

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

class NewsSpider(CrawlSpider):
    name = 'XXXspider'
    allowed_domains = ['XXX.com']
    start_urls = [
        "http://XXX_URL",
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'^http://XXX.com/XXX_URL')), callback="parse_XXX"),
        # and so on...
    )
    def parse_XXX(self, response):
        hxs = HtmlXPathSelector(response) 
        hxs = HtmlXPathSelector(text = "XXX_STRING")
        hxs.select("//div[@class='XXX']/*").extract()
        hxs.select("//div[@class='XXX']/text()").extract()
        hxs.select("//div[@class='XXX']//p").extract() # 不考虑位置地获得所有的p
        for sel in hxs.select("//div[@class='XXX']"):
            sel.select("//p").extract()
        return [item]

# 写pipline
# settings里指定pipeline
ITEM_PIPELINES = ['XXXProject.pipelines.XXXPipeline']

class XXXPipeline(object):
    def __init__(self):
        self.conn = pymongo.Connection(host='127.0.0.1',port=27017)
    def process_item(self, item, spider):
        self.conn.scrapydb.news.update({"title" : item["title"]}, {"$set" : dict(item)}, upsert = True, multi=False)
        return item
