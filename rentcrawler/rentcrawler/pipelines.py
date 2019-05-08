import csv
from scrapy.exceptions import DropItem


class CsvPipeline(object):

    def __init__(self):
        self.pointsBj = []
        self.pointsBj_detail = []
        self.pointsSh = []
        self.pointsSh_detail = []
        self.pointsGz = []
        self.pointsGz_detail = []
        self.pointsSz = []
        self.pointsSz_detail = []
        self.pointsCd = []
        self.pointsCd_detail = []


    def process_item(self, item, spider):

        dic = {
            "title": item['house_title'],
            "location": item['house_location'],
            "lnglat": item['house_lnglat'],
            "url": item['house_url']
        }
        dic_detail = {
            "title": item['house_title'],
            "location": item['house_location'],
            "lnglat": item['house_lnglat'],
            "size": item['house_size'],
            "orient": item['house_orient'],
            "type": item['house_type'],
            "time": item['house_time'],
            "price": item['house_price'],
            "image": item['house_image'],
            "url": item['house_url']
        }

        if item['house_city'] == '北京':
            self.pointsBj.append(dic)
            self.pointsBj_detail.append(dic_detail)
        elif item['house_city'] == '上海':
            self.pointsSh.append(dic)
            self.pointsSh_detail.append(dic_detail)
        elif item['house_city'] == '广州':
            self.pointsGz.append(dic)
            self.pointsGz_detail.append(dic_detail)
        elif item['house_city'] == '深圳':
            self.pointsSz.append(dic)
            self.pointsSz_detail.append(dic_detail)
        elif item['house_city'] == '成都':
            self.pointsCd.append(dic)
            self.pointsCd_detail.append(dic_detail)


        return item

    def close_spider(self, spider):
        with open('LianjiaBj.js', 'a+', encoding='utf-8') as f:
            f.write('var points = ')
            f.write(str(self.pointsBj))
        with open('LianjiaBj_detail.js', 'a+', encoding='utf-8') as f:
            f.write('var points = ')
            f.write(str(self.pointsBj_detail))


        with open('LianjiaSh.js', 'a+', encoding='utf-8') as f:
            f.write('var points = ')
            f.write(str(self.pointsSh))
        with open('LianjiaSh_detail.js', 'a+', encoding='utf-8') as f:
            f.write('var points = ')
            f.write(str(self.pointsSh_detail))


        with open('LianjiaGz.js', 'a+', encoding='utf-8') as f:
            f.write('var points = ')
            f.write(str(self.pointsGz))
        with open('LianjiaGz_detail.js', 'a+', encoding='utf-8') as f:
            f.write('var points = ')
            f.write(str(self.pointsGz_detail))


        with open('LianjiaSz.js', 'a+', encoding='utf-8') as f:
            f.write('var points = ')
            f.write(str(self.pointsSz))
        with open('LianjiaSz_detail.js', 'a+', encoding='utf-8') as f:
            f.write('var points = ')
            f.write(str(self.pointsSz_detail))


        with open('LianjiaCd.js', 'a+', encoding='utf-8') as f:
            f.write('var points = ')
            f.write(str(self.pointsCd))
        with open('LianjiaCd_detail.js', 'a+', encoding='utf-8') as f:
            f.write('var points = ')
            f.write(str(self.pointsCd_detail))





