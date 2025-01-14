import csv
import datetime

from scrapy.exceptions import DropItem
import pymysql
import re, time
from rentcrawler.items import HouseItem
import requests

'''
    数据预处理
'''
class ParsePipeline():

    #   时间格式规范化
    def parse_time(self, date):

        #   链家发布时间格式处理
        if re.match('今天', date):
            date = time.strftime('%Y-%m-%d', datetime.datetime.now())
        if re.match('\d+天前', date):
            date = time.strftime('%Y-%m-%d', datetime.datetime.now())
            n = re.match('(\d+)', date).group(1)
            delta = datetime.timedelta(days=n)
            date = time.strftime('%Y-%m-%d', (date - delta).strftime('%Y-%m-%d'))
        if re.match('\d+个月前', date):
            date = time.strftime('%Y-%m-%d', datetime.datetime.now())
            n = re.match('(\d+)', date).group(1)
            delta = datetime.timedelta(months=n) * 30
            date = time.strftime('%Y-%m-%d', (date - delta).strftime('%Y-%m-%d'))
        if re.match('\d+年前', date):
            date = time.strftime('%Y-%m-%d', datetime.datetime.now())
            n = re.match('(\d+)', date).group(1)
            delta = datetime.timedelta(years=n) * 365
            date = time.strftime('%Y-%m-%d', (date - delta).strftime('%Y-%m-%d'))

        #   安居客发布时间格式处理
        if re.match('\d+年\d+月\d+日', date):
            y = re.match('(\d+)年', date).group(1)
            m = re.match('(\d+)月', date).group(1)
            d = re.match('(\d+)日', date).group(1)
            date = y + '-' + m + '-' +d
        return date

    #   经纬度格式规范化
    def geocode(self, address):
        parameters = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
        base = 'http://restapi.amap.com/v3/geocode/geo'
        response = requests.get(base, parameters)
        answer = response.json()
        lnglat = answer['geocodes'][0]['location']
        print(address + "的经纬度：", lnglat)
        return lnglat

    def process_item(self, item, spider):
        if isinstance(item, HouseItem):
            if item.get('house_time'):
                item['house_time'] = item['house_time'].strip()
                item['house_time'] = self.parse_time(item.get('house_time'))
            if item.get('house_location'):
                item['house_location'] = item['house_location'].strip()
                item['house_lnglat'] = self.geocode(item['house_location'])
            if re.match('未知', item.get['house_type']):
                raise DropItem("Missing type in %s" % item)


        return item



"""
    存储到MySQL
"""
class MySQLPipeline():

    def __init__(self, host, database, user, password, port):

        # Mysql数据库配置
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.db = pymysql.connect(self.host, self.user, self.password, self.database)
        self.cursor = self.db.cursor()

        # 第一批：北京、上海、广州、深圳、成都
        # self.pointsBj = []
        # self.pointsBj_detail = []
        # self.pointsSh = []
        # self.pointsSh_detail = []
        # self.pointsGz = []
        # self.pointsGz_detail = []
        # self.pointsSz = []
        # self.pointsSz_detail = []
        # self.pointsCd = []
        # self.pointsCd_detail = []

        # 第二批：天津、南京、杭州、青岛、西安、厦门、合肥、重庆、武汉
        # self.pointsTj = []
        # self.pointsNj = []
        # self.pointsHz = []
        # self.pointsQd = []
        # self.pointsXa = []
        # self.pointsXm = []
        # self.pointsHf = []
        # self.pointsCq = []
        # self.pointsWh = []

        # 第三批：长沙
        # self.pointsCs = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def process_item(self, item, spider):

        city = item['house_city']
        title = item['house_title']
        location = item['house_location']
        lnglat = item['house_lnglat']
        size = item['house_size']
        orient = item['house_orient']
        type = item['house_type']
        time = item['house_time']
        price = item['house_price']
        image = item['house_image']
        url = item['house_url']
        refer = item['house_refer']
        area = item['house_area']

        if item['house_city'] == '北京':
            sql = 'insert into bj (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '重庆':
            sql = 'insert into cq (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '成都':
            sql = 'insert into cd (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '长沙':
            sql = 'insert into cs (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '广州':
            sql = 'insert into gz (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '合肥':
            sql = 'insert into hf (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '杭州':
            sql = 'insert into hz (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '南京':
            sql = 'insert into nj (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '青岛':
            sql = 'insert into qd (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '上海':
            sql = 'insert into sh (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '深圳':
            sql = 'insert into sz (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '天津':
            sql = 'insert into tj (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '武汉':
            sql = 'insert into wh (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '西安':
            sql = 'insert into xa (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        elif item['house_city'] == '厦门':
            sql = 'insert into xm (city, title, area, location, lnglat, size, orient, type, time, price, image, url, refer) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        # data = dict(item)
        # keys = ','.join(data.keys())
        # values = ','.join(['%s'] * len(data))
        # sql = 'insert into %s (%s) values (%s)' % ('house', keys, values)

        self.cursor.execute(sql, (city, title, area, location, str(lnglat), size, orient, type, time, price, image, url, refer))
        self.db.commit()

        # dic = {
        #     "title": item['house_title'],
        #     # "location": item['house_location'],
        #     "lnglat": item['house_lnglat'],
        #     "url": item['house_url']
        # }

        # ⤵️这个太复杂，占空间太多，弃用
        # dic_detail = {
        #     "title": item['house_title'],
        #     "location": item['house_location'],
        #     "lnglat": item['house_lnglat'],
        #     "size": item['house_size'],
        #     "orient": item['house_orient'],
        #     "type": item['house_type'],
        #     "time": item['house_time'],
        #     "price": item['house_price'],
        #     "image": item['house_image'],
        #     "url": item['house_url']
        # }

        # 第一批：北京、上海、广州、深圳、成都
        # if item['house_city'] == '北京':
        #     self.pointsBj.append(dic)
        #     self.pointsBj_detail.append(dic_detail)
        # elif item['house_city'] == '上海':
        #     self.pointsSh.append(dic)
        #     self.pointsSh_detail.append(dic_detail)
        # elif item['house_city'] == '广州':
        #     self.pointsGz.append(dic)
        #     self.pointsGz_detail.append(dic_detail)
        # elif item['house_city'] == '深圳':
        #     self.pointsSz.append(dic)
        #     self.pointsSz_detail.append(dic_detail)
        # elif item['house_city'] == '成都':
        #     self.pointsCd.append(dic)
        #     self.pointsCd_detail.append(dic_detail)

        # 第二批：天津、南京、杭州、青岛、西安、厦门、合肥、重庆、武汉
        # if item['house_city'] == '天津':
        #     self.pointsTj.append(dic)
        # elif item['house_city'] == '南京':
        #     self.pointsNj.append(dic)
        # elif item['house_city'] == '杭州':
        #     self.pointsHz.append(dic)
        # elif item['house_city'] == '青岛':
        #     self.pointsQd.append(dic)
        # elif item['house_city'] == '西安':
        #     self.pointsXa.append(dic)
        # elif item['house_city'] == '厦门':
        #     self.pointsXm.append(dic)
        # elif item['house_city'] == '合肥':
        #     self.pointsHf.append(dic)
        # elif item['house_city'] == '重庆':
        #     self.pointsCq.append(dic)
        # elif item['house_city'] == '武汉':
        #     self.pointsWh.append(dic)

        # 第三批：长沙
        # if item['house_city'] == '长沙':
        #     self.pointsCs.append(dic)

        return item

    def close_spider(self, spider):

        self.db.close()
        # 第一批：北京、上海、广州、深圳、成都
        # with open('LianjiaBj.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points = ')
        #     f.write(str(self.pointsBj))
        # with open('LianjiaBj_detail.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points = ')
        #     f.write(str(self.pointsBj_detail))
        #
        #
        # with open('LianjiaSh.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points = ')
        #     f.write(str(self.pointsSh))
        # with open('LianjiaSh_detail.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points = ')
        #     f.write(str(self.pointsSh_detail))
        #
        #
        # with open('LianjiaGz.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points = ')
        #     f.write(str(self.pointsGz))
        # with open('LianjiaGz_detail.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points = ')
        #     f.write(str(self.pointsGz_detail))
        #
        #
        # with open('LianjiaSz.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points = ')
        #     f.write(str(self.pointsSz))
        # with open('LianjiaSz_detail.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points = ')
        #     f.write(str(self.pointsSz_detail))
        #
        #
        # with open('LianjiaCd.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points = ')
        #     f.write(str(self.pointsCd))
        # with open('LianjiaCd_detail.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points = ')
        #     f.write(str(self.pointsCd_detail))


        # 第二批：天津、南京、杭州、青岛、西安、厦门、合肥、重庆、武汉
        # with open('LianjiaTj.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points_tj = ')
        #     f.write(str(self.pointsTj))
        #
        # with open('LianjiaNj.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points_nj = ')
        #     f.write(str(self.pointsNj))
        #
        # with open('LianjiaHz.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points_hz = ')
        #     f.write(str(self.pointsHz))
        #
        # with open('LianjiaQd.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points_qd = ')
        #     f.write(str(self.pointsQd))
        #
        # with open('LianjiaXa.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points_xa = ')
        #     f.write(str(self.pointsXa))
        #
        # with open('LianjiaXm.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points_xm = ')
        #     f.write(str(self.pointsXm))
        #
        # with open('LianjiaHf.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points_hf = ')
        #     f.write(str(self.pointsHf))
        #
        # with open('LianjiaCq.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points_cq = ')
        #     f.write(str(self.pointsCq))
        #
        # with open('LianjiaWh.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points_wh = ')
        #     f.write(str(self.pointsWh))

        # 第三批：长沙
        # with open('LianjiaCs.js', 'a+', encoding='utf-8') as f:
        #     f.write('var points_cs = ')
        #     f.write(str(self.pointsCs))

