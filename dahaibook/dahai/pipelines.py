# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.exceptions import DropItem
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class DahaiPipeline(object):
    def process_item(self, item, spider):
        print item['title']
        words_ = item['title'].split('_')
        words = [x.strip() for x in words_]
        #正文 第450章 离家不走_透视神医在花都_都市小说_大海中文
        if len(words) != 4:
            raise DropItem("Item not usual "+ item['title'])
        if not os.path.exists(words[2]):
            os.mkdir(words[2])
        bookdir = os.path.join(words[2], words[1])
        if not os.path.exists(bookdir):
            os.mkdir(bookdir)
        with open(os.path.join(bookdir, words[0]), 'w') as file:
            for u in item['booktext']:
                file.write(u + '\n')
        return item
