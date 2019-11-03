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
        # 还不是很理解对 HtmlXPathSelector 选择 / 是什么意思??????
        # hxs 本身是一个 HtmlXPathSelector, 它的 select的返回值也是 HtmlXPathSelector?????
        # 但是如果加了绝对路径，就会不限制在这个点上了， 我觉得得用相对路径才行
        hxs.select("//div[@class='XXX']/*").extract()
        hxs.select("//div[@class='XXX']/text()").extract()
        hxs.select("//div[@class='XXX']/@ATTR").extract() # 提取属性
        hxs.select("//div[@class='XXX']//p").extract() # 不考虑位置地获得所有的p
        # Tips: chrome 开发者界面中可以 右键点击元素， 然后 copy xpath。 https://stackoverflow.com/a/42194160
        for sel in hxs.select("//div[@class='XXX']"):
            sel.select("//p").extract()

        # NOTE: xpath 坑
        # 如果有的属性不是完全相等，而是包含， 需要这样才能匹配到： '//table[contains(@class, "infobox")]//img'
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

# Requests-HTML: HTML Parsing for Humans™
# https://github.com/kennethreitz/requests-html


