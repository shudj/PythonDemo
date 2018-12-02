# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor
from time import ctime,sleep
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor
from toMysql.items import TomysqlItem
from scrapy.http import Request
import logging
import pymysql
import scrapy
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc


class SinanewsSpider(scrapy.Spider):
    name = "sns"
    start_urls = []

    def __init__(self):
        self.start_urls = ["http://roll.news.sina.com.cn/news/gnxw/gdxw1/index.shtml"]

    def parse(self, response):
        for url in response.xpath('//ul/li/a/@href').extract():
            yield scrapy.Request(url, callback=self.parse_detail)

        nextLink = []
        nextLink = response.xpath('//div[@class="pagebox"]/span[last()-1/a/@href]').extract()
        if nextLink:
            nextLink = nextLink[0]
            nextpage = nextLink.split('./')[1]
            yield Request("http://roll.news.sina.com.cn/news/gnxw/gdxw1/" + nextpage, callback=self.parse)

    def parse_detail(self, response):
        item = TomysqlItem()
        item['title'] = response.xpath('//h1[@class="main-title"]/text()').extract()[0]
        content = ''
        for con in response.xpath('//div[@id="article"]/p/text()').extract():
            content = content + con
        item["content"] = content
        item['pubtime'] = response.xpath('//span[@class="date"]/text()').extract()[0]
        imageurl = ''
        for img in response.xpath('//div[@id="article"]/div[@class="img_wrapper"]/img/@src').extract():
            imageurl = imageurl + img + '|'
        item['imageUrl'] = imageurl
        item['url'] = response.url
        yield item

