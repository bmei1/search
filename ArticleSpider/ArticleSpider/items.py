# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()  # encode to unique length
    author = scrapy.Field()
    author_description = scrapy.Field()
    applause = scrapy.Field()
    content = scrapy.Field()
    # front_pic_url = scrapy.Field()
    # front_pic_path = scrapy.Field()