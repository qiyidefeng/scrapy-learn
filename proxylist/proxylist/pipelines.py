# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyTestPipeline(object):
    def __init__(self):
        self.file = open('proxylist.txt', 'a')

    def process_item(self, item, spider):
        self.file.write(item['ip'] + ':' + item['port'] + '\n')
        return item
