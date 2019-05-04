import csv
from scrapy.exceptions import DropItem


class CsvPipeline(object):

    def process_item(self, item, spider):

        with open('rent.csv', 'a+', encoding='utf-8') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow([item['house_title'], item['house_location'], item['house_area'],
                                 item['house_size'], item['house_orientation'], item['house_type'],
                                 item['house_time'], item['house_price'], item['house_image'],
                                 item['house_url']])

        return item


class DuplicatesPipeline(object):
    """
    去除重复房源
    """

    def __init__(self):
        self.house_set = set()

    def process_item(self, item, spider):
        title = item['title']
        if title in self.house_set:
            raise DropItem('Duplicate house found:%s' % item)

        self.house_set.add(title)
        return item





