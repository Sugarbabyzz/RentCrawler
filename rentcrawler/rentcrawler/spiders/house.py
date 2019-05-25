# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from rentcrawler.items import HouseItem
from urllib import parse


class HouseSpider(scrapy.Spider):

    name = 'house'
    start_urls = [ #'https://cs.lianjia.com/zufang/',
                   # 'https://tj.lianjia.com/zufang/',
                   # 'https://nj.lianjia.com/zufang/',
                   # 'https://hz.lianjia.com/zufang/',
                   # 'https://qd.lianjia.com/zufang/',
                   # 'https://xa.lianjia.com/zufang/',
                   'https://xm.lianjia.com/zufang/',
                   # 'https://hf.lianjia.com/zufang/',
                   # 'https://cq.lianjia.com/zufang/',
                   # 'https://wh.lianjia.com/zufang/',
                   # 'https://bj.lianjia.com/zufang/',
                   # 'https://sh.lianjia.com/zufang/',
                   # 'https://gz.lianjia.com/zufang/',
                   'https://sz.lianjia.com/zufang/',
                   # 'https://cd.lianjia.com/zufang/'
                 ]
    # 第一批
    # 北京19856 + 上海24265 + 广州44235 + 深圳28373 + 成都83762 = 200491   实际 183749

    # 第二批
    # 天津21084 + 南京61906 + 杭州57769 + 青岛33840 + 西安33564 + 厦门10591 + 合肥20304 + 重庆31656 + 武汉86444 = 357158   实际

    # 第三批
    # 长沙21675

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
        item = HouseItem()

        # item['house_city'] = response.xpath('//p[@class="bread__nav__wrapper oneline"]/a/text()').re_first('(.*)租房网')
        # item['house_title'] = (response.xpath('//p[contains(@class, "title")]/text()').extract_first()).replace(' ',
        #                                                                                                         '').replace(
        #     '\n', '').replace('，', ' ').replace('。', '')
        # item['house_lnglat'] = []
        # item['house_lnglat'].append(response.xpath('/html/body/div[3]/script/text()').re_first('longitude: \'(.*)\''))
        # item['house_lnglat'].append(response.xpath('/html/body/div[3]/script/text()').re_first('latitude: \'(.*)\''))
        # item['house_location'] = response.xpath('/html/body/div[3]/script/text()').re_first('g_conf.name = \'(.*)\'')
        # item['house_orient'] = response.xpath('//div[@id="aside"]/ul[1]/p/span[4]/text()').extract_first()
        # item['house_size'] = response.xpath('//div[@id="aside"]/ul[1]/p/span[3]/text()').extract_first()
        # item['house_type'] = response.xpath('//div[@id="aside"]/ul[1]/p/span[2]/text()').extract_first()
        # item['house_time'] = response.xpath('//div[@class="content__article__info"]/ul/li[2]/text()').re_first('发布：(.*)')
        # item['house_price'] = response.xpath('//div[@id="aside"]/p[1]/span/text()').extract_first()
        # item['house_image'] = response.xpath('//ul[@id="prefix"]/li[1]/img/@src').extract_first()
        # item['house_url'] = response.url

        item['house_city'] = response.xpath('//p[@class="bread__nav__wrapper oneline"]/a/text()').re_first('(.*)租房网')
        item['house_title'] = (response.xpath('//p[contains(@class, "title")]/text()').extract_first()).replace(' ',
                                                                                                                '').replace(
            '\n', '').replace('，', ' ').replace('。', '')
        item['house_lnglat'] = []
        item['house_lnglat'].append(response.xpath('/html/body/div[3]/script/text()').re_first('longitude: \'(.*)\''))
        item['house_lnglat'].append(response.xpath('/html/body/div[3]/script/text()').re_first('latitude: \'(.*)\''))
        item['house_location'] = response.xpath('/html/body/div[3]/script/text()').re_first('g_conf.name = \'(.*)\'')
        item['house_orient'] = response.xpath('//div[@id="aside"]/ul[1]/p/span[4]/text()').extract_first()
        item['house_size'] = response.xpath('//div[@id="aside"]/ul[1]/p/span[3]/text()').re_first('(.*)㎡')
        item['house_type'] = response.xpath('//div[@id="aside"]/ul[1]/p/span[2]/text()').extract_first()
        item['house_time'] = response.xpath('//div[@class="content__subtitle"]/text()').re_first('房源上架时间(.*)').strip()
        item['house_price'] = response.xpath('//div[@id="aside"]/p[1]/span/text()').extract_first()
        item['house_image'] = response.xpath('//ul[@id="prefix"]/li[1]/img/@src').extract_first()
        item['house_url'] = response.url
        item['house_refer'] = '链家'

        yield item





