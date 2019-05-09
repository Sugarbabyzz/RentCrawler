import csv
from scrapy.exceptions import DropItem


class CsvPipeline(object):

    def __init__(self):

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
        self.pointsCs = []

    def process_item(self, item, spider):

        dic = {
            "title": item['house_title'],
            # "location": item['house_location'],
            "lnglat": item['house_lnglat'],
            "url": item['house_url']
        }

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
        if item['house_city'] == '长沙':
            self.pointsCs.append(dic)

        return item

    def close_spider(self, spider):
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
        with open('LianjiaCs.js', 'a+', encoding='utf-8') as f:
            f.write('var points_cs = ')
            f.write(str(self.pointsCs))






