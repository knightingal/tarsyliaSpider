import scrapy
from scrapy.selector import Selector


class TarsyliaSpider(scrapy.Spider):
    name = 'tarsylia'
    section_index = 0
    book_index = 0
    image_index = 0

    def start_requests(self):
        urls = ['http://tarsyliatales.com/category/comic']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        inner_selectors = Selector(response=response).xpath('//div[@class="book-inner"][position()<10]')
        for inner_selector in inner_selectors:
            index = inner_selectors.index(inner_selector)
            title = inner_selector.xpath('h4[1]/text()').extract()[0]
            intro_src = inner_selector.xpath('.//div[@class="intro"]//img/@src').extract()[0]
            intro_text = inner_selector.xpath('.//div[@class="intro-text"][1]/text()').extract()[0].strip()
            section_count = inner_selector.xpath('.//ul/li[3]/text()').extract()[0]

            section_selectors = inner_selector.xpath('.//div[@class="post-list"]/a')

            for section_selector in section_selectors:
                href = section_selector.xpath('./@href').extract()[0]
                name = section_selector.xpath('./text()').extract()[0]
                yield {'table': 'section', 'index_in_book': section_selectors.index(section_selector),
                       'url': href, 'book_id': self.book_index, 'name': name, 'id': self.section_index}
                request = scrapy.Request(href, callback=self.parse_section)
                request.meta['section_id'] = self.section_index
                self.section_index += 1
                yield request

            yield {'id': self.book_index, 'title': title, 'intro_src': intro_src, 'intro_text': intro_text,
                   'section_count': section_count, 'table': "book"}
            self.book_index += 1

    def parse_section(self, response):
        image_srcs = Selector(response=response).xpath('//ul[@id="imageGallery"][1]/li/@data-src').extract()
        for image_src in image_srcs:
            yield {'table': 'image',
                   'index_in_section': image_srcs.index(image_src),
                   'id': self.image_index,
                   'src': image_src,
                   'section_id': response.meta['section_id']}
            self.image_index += 1


