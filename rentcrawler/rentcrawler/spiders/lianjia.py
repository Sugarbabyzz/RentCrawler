# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from rentcrawler.items import LianjiaItem


class LianjiaSpider(scrapy.Spider):

    name = 'lianjia'
    start_urls = ['https://bj.lianjia.com/zufang/']

    def parse(self, response):
        item = LianjiaItem()

        html = response.xpath('//div[@class="content__list"]/div')

        for i in html:

            item['house_title'] = (i.xpath('div//p[contains(@class, "title")]/a/text()').extract_first()).replace(' ', '').replace('\n', '').replace('，', ' ').replace('。', '')
            item['house_location'] = i.xpath('div//p[contains(@class, "des")]/a[1]/text()').extract_first()
            item['house_area'] = i.xpath('div//p[contains(@class, "des")]/a[2]/text()').extract_first()
            item['house_orientation'] = "南"
            item['house_size'] = "200"
            item['house_type'] = "整租"
            item['house_time'] = i.xpath('div//p[contains(@class, "time")]/text()').extract_first()
            item['house_price'] = (i.xpath('div//span[contains(@class, "price")]/em/text()').extract_first()
                                  + i.xpath('div//span[contains(@class, "price")]/text()').extract_first()).replace(' ', '')
            item['house_image'] = i.xpath('div/a/img/@src').extract_first()
            # item['house_url'] = i.urljoin(response.xpath('div/a/@href'))
            item['house_url'] = "222"

            yield item

        for i in range(2, 5):
            url = 'https://bj.lianjia.com/zufang/pg{}'.format(str(i))
            yield Request(url, callback=self.parse)







