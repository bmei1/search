# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ArticleSpider.items import ArticlespiderItem
from ArticleSpider.utils.common import get_md5
import datetime
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class MediumSpider(scrapy.Spider):
    name = 'medium'
    allowed_domains = ['medium.com']
    # start_urls = ['https://medium.com/search?q=machine%20learning']
    start_urls = ['https://medium.com/tag/data-science/latest']

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="/Users/meibing/Desktop/search/ArticleSpider/chromedriver")
        super(MediumSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print("spider closed")
        self.browser.quit()

    def parse(self, response):

        # post_nodes = response.css(".postArticle-content a")  # select the div of each article
        post_nodes = response.css(".postArticle-readMore a")

        for post_node in post_nodes:
            post_url = post_node.css("::attr(href)").extract_first("")

            # pic_url = post_node.css("img::attr(data-src)").extract_first("")
            # yield Request(url=post_url, meta={'front_pic_url': pic_url}, callback=self.parse_detail, dont_filter=True)
            yield Request(url=post_url, callback=self.parse_detail, dont_filter=True)

    #get detail of each article
    def parse_detail(self, response):

        # try:
        #     response.find_element_by_css_selector(".overlay.overlay--lighter button.button.button--close").click()
        # # time.sleep(1)
        # except:
        #     pass

        article_item = ArticlespiderItem()

        # front_pic_url = response.meta.get("front_pic_url", "")  # use get for Exception
        title = response.css(".section-inner.sectionLayout--insetColumn h1 ::text").extract_first("")
        create_date = response.css(".ui-caption.postMetaInline time::attr(datetime)").extract_first("")[:10]
        author = response.css(".u-lineHeightTightest a::text").extract_first("")
        author_description = response.css(".ui-caption.ui-xs-clamp2.postMetaInline ::text").extract_first("")
        applause = response.css(".button.button--chromeless.u-baseColor--buttonNormal ::text").extract_first("")
        content = " ".join(response.css(".section-inner.sectionLayout--insetColumn p.graf.graf--p::text").extract())

        article_item["title"] = title
        article_item["url"] = response.url
        article_item["url_object_id"] = get_md5(response.url)

        try:
            create_date = datetime.datetime.strptime(create_date, "%Y-%m-%d").date()
        except Exception as e:
            create_date = None
        article_item["create_date"] = create_date

        article_item["author"] = author
        article_item["author_description"] = author_description

        if "K" in applause:
            applause = int(float(applause.strip("K")) * 1000)
        else:
            applause = int(applause)
        article_item["applause"] = applause

        article_item["content"] = content
        # article_item["front_pic_url"] = [front_pic_url]  # need list

        yield article_item
