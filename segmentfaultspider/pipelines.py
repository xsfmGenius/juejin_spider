# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql
from segmentfaultspider.items import SegmentfaultspiderItem

class SegmentfaultspiderPipeline(object):
    def __init__(self):
        self.connection=pymysql.connect(host='192.168.0.136',
                port=3306,
                user='root',
                password='1122334455',
                db='userspider',
                charset='utf8mb4')
    def process_item(self, item, spider):
        if isinstance(item, SegmentfaultspiderItem):
            self.cursor = self.connection.cursor()
            try:
                self.cursor.execute('INSERT INTO users (`name`,`up`,`read`,`reputation`,`followA`,`Afollow`,`time`,`loc`,`company`,`introduce`) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(item["name"],item["up"],item["read"],item["reputation"],item["followA"],item["Afollow"],item["time"],item["loc"],item["company"],item["introduce"]))
                self.connection.commit()
            except Exception as e:
                print(e)
                self.connection.rollback()
    #
    # def close_spider(self,spider):
    #     self.cursor.close()
    #     self.connection.close()
