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
    # 北京19856 + 上海24265 + 广州44235 + 深圳28373 + 成都83762 = 200491   实际 183749

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.location_parse)

    """
    选择城区
    """
    def location_parse(self, response):

        html = response.xpath('//div[@id="filter"]/ul[2]/li[not(@data-id="0")]')

        for li in html:
            url = parse.urljoin(response.url, li.xpath('a/@href').extract_first())
            yield Request(url=url, callback=self.area_parse)

    """
    选择街区
    """
    def area_parse(self, response):

        html = response.xpath('//div[@id="filter"]/ul[4]/li[not(@data-id="0")]')

        for li in html:
            url = parse.urljoin(response.url, li.xpath('a/@href').extract_first())
            yield Request(url=url, callback=self.page_parse)

    """
    选择页码
    """
    def page_parse(self, response):

        total_page = response.xpath('//div[@class="content__pg"]/@data-totalpage').extract_first()

        for i in range(1, int(total_page) + 1):
            url = str(response.url) + 'pg{}'.format(str(i))
            yield Request(url=url, callback=self.house_parse)

    """
    选择房源
    """
    def house_parse(self, response):

        html = response.xpath('//div[@class="content__list"]/div')

        for div in html:
            url = parse.urljoin(response.url, div.xpath('a/@href').extract_first())
            yield Request(url=url, callback=self.house_detail_parse)

    """
    抓取房源细节信息
    """
    def house_detail_parse(self, response):
        item = LianjiaItem()

        item['house_city'] = response.xpath('//p[@class="bread__nav__wrapper oneline"]/a/text()').re_first('(.*)租房网')
        item['house_title'] = (response.xpath('//p[contains(@class, "title")]/text()').extract_first()).replace(' ',
                                                                                                                '').replace(
            '\n', '').replace('，', ' ').replace('。', '')
        item['house_lnglat'] = []
        item['house_lnglat'].append(response.xpath('/html/body/div[3]/script/text()').re_first('longitude: \'(.*)\''))
        item['house_lnglat'].append(response.xpath('/html/body/div[3]/script/text()').re_first('latitude: \'(.*)\''))
        item['house_location'] = response.xpath('/html/body/div[3]/script/text()').re_first('g_conf.name = \'(.*)\'')
        item['house_orient'] = response.xpath('//div[@id="aside"]/ul[1]/p/span[4]/text()').extract_first()
        item['house_size'] = response.xpath('//div[@id="aside"]/ul[1]/p/span[3]/text()').extract_first()
        item['house_type'] = response.xpath('//div[@id="aside"]/ul[1]/p/span[2]/text()').extract_first()
        item['house_time'] = response.xpath('//div[@class="content__article__info"]/ul/li[2]/text()').re_first('发布：(.*)')
        item['house_price'] = response.xpath('//div[@id="aside"]/p[1]/span/text()').extract_first()
        item['house_image'] = response.xpath('//ul[@id="prefix"]/li[1]/img/@src').extract_first()
        item['house_url'] = response.url

        yield item

