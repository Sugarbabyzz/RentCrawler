# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from rentcrawler.items import LianjiaItem
from urllib import parse


class LianjiaSpider(scrapy.Spider):

    name = 'lianjia'
    start_urls = ['https://bj.lianjia.com/zufang/',
                  'https://sh.lianjia.com/zufang/',
                  'https://gz.lianjia.com/zufang/',
                  'https://sz.lianjia.com/zufang/',
                  'https://cd.lianjia.com/zufang/'
                  ]
    # 北京19856 + 上海24265 + 广州44235 + 深圳28373 + 成都83762 = 200491

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.location_parse)

    def location_parse(self, response):

        html = response.xpath('//div[@id="filter"]/ul[2]/li[not(@data-id="0")]')

        for li in html:
            url = parse.urljoin(response.url, li.xpath('a/@href').extract_first())
            yield Request(url=url, callback=self.area_parse)

    def area_parse(self, response):

        html = response.xpath('//div[@id="filter"]/ul[4]/li[not(@data-id="0")]')

        for li in html:
            url = parse.urljoin(response.url, li.xpath('a/@href').extract_first())
            yield Request(url=url, callback=self.page_parse)

    def page_parse(self, response):

        total_page = response.xpath('//div[@class="content__pg"]/@data-totalpage').extract_first()

        for i in range(1, int(total_page) + 1):
            url = str(response.url) + 'pg{}'.format(str(i))
            yield Request(url=url, callback=self.house_parse)

    def house_parse(self, response):
        item = LianjiaItem()
        item['house_city'] = response.xpath('//p[@class="bread__nav__wrapper oneline"]/a/text()').re_first('链家网(.*)站')

        html = response.xpath('//div[@class="content__list"]/div')

        for i in html:

            item['house_title'] = (i.xpath('div//p[contains(@class, "title")]/a/text()').extract_first()).replace(' ', '').replace('\n', '').replace('，', ' ').replace('。', '')
            item['house_location'] = i.xpath('div//p[contains(@class, "des")]/a[1]/text()').extract_first()
            item['house_area'] = i.xpath('div//p[contains(@class, "des")]/a[2]/text()').extract_first()
            item['house_orientation'] = i.xpath('div//p[contains(@class, "des")]/text()[5]').extract_first().replace(' ', '').replace('\n', '')
            item['house_size'] = i.xpath('div//p[contains(@class, "des")]/text()[4]').extract_first().replace(' ', '').replace('\n', '')
            item['house_type'] = i.xpath('div//p[contains(@class, "des")]/text()[6]').extract_first().replace(' ', '').replace('\n', '')
            item['house_time'] = i.xpath('div//p[contains(@class, "time")]/text()').extract_first()
            item['house_price'] = (i.xpath('div//span[contains(@class, "price")]/em/text()').extract_first()
                                  + i.xpath('div//span[contains(@class, "price")]/text()').extract_first()).replace(' ', '')
            item['house_image'] = i.xpath('a//img/@data-src').extract_first()
            item['house_url'] = parse.urljoin(response.url, i.xpath('div//p[contains(@class, "title")]/a/@href').extract_first())

            yield item








