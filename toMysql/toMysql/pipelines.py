# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#CREATE TABLE SinaLocalNews (
#id int(11) NOT NULL AUTO_INCREMENT,
#    ->   title VARCHAR(100),
#   ->   content  TEXT,
#  ->   imageUrl       VARCHAR(2000),
# ->   Url    VARCHAR(1000),
#->   pubtime  DATETIME,
#    ->   PRIMARY KEY (id)
#   -> ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
import pymysql


class TomysqlPipeline(object):
    con = pymysql.connect(host='localhost', port=3306, user='Iothub', password='Iothub', db='sinanews', charset='utf8')
    cur = con.cursor()

    def process_item(self, item, spider):
        sql = "insert into SinaLocalNews(title, content, imageUrl, Url, pubtime) VALUES(%s, %s, %s, %s, " \
              "trim(replace(replace(replace(left(%s, 16), '年', '-'), '月', '-'), '日', '')))"

        self.cur.execute(sql, (item['title'], item['content'], item['imageUrl'],item['url'], item['pubtime']))
        self.con.commit
        return item
