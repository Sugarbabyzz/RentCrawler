# -*- coding: utf-8 -*-
import scrapy


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['www.lianjia.com']
    start_urls = ['http://www.lianjia.com/']

    def parse(self, response):
        pass
