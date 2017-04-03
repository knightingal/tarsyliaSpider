# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector


class TarsyliaPipeline(object):

    def __init__(self, uri, db, user_name, password):
        self.uri = uri
        self.db = db
        self.user_name = user_name
        self.password = password
        self.cnx = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get("HOST"),
            crawler.settings.get("NAME"),
            crawler.settings.get("USER"),
            crawler.settings.get("PASSWORD")
        )

    insert_book = (
        "INSERT INTO tarsylia_book (id, title, intro_src, intro_text, section_count)"
        "VALUES (%s, %s, %s, %s, %s)"
    )

    insert_section = (
        'insert into tarsylia_section (id, url, book_id, name, index_in_book)'
        'values (%s, %s, %s, %s, %s)'
    )

    insert_img = (
        'insert into tarsylia_img (id, index_in_section, section_id, src)'
        'values (%s, %s, %s, %s)'
    )

    def process_item(self, item, spider):
        cur = self.cnx.cursor(buffered=True)
        if item['table'] == 'book':
            cur.execute(self.insert_book, (
                item["id"],
                item["title"],
                item["intro_src"],
                item["intro_text"],
                item["section_count"]
            ))
        elif item['table'] == 'section':
            cur.execute(self.insert_section, (
                item['id'], item['url'], item['book_id'], item['name'], item['index_in_book']
            ))
        else:
            cur.execute(self.insert_img, (
                item['id'], item['index_in_section'], item['section_id'], item['src']
            ))

        return item

    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(user=self.user_name, password=self.password, database=self.db, host=self.uri)

    def close_spider(self, spider):
        self.cnx.commit()
        self.cnx.close()
