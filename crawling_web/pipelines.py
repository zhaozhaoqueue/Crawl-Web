# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class CrawlingWebPipeline(object):
    def process_item(self, item, spider):
        full_name = item["full_name"]
        name_note = full_name.split('(', 1)
        item["full_name"] = name_note[0]
        item["note"] = "".join(name_note[1:])
        return item