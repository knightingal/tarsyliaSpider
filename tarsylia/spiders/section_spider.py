import scrapy
from scrapy.selector import Selector

class SectionSpider(scrapy.Spider):
    name = 'section'

    def start_requests(self):
        urls = ['http://tarsyliatales.com/181']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        image_gallerys = Selector(response=response).xpath('//ul[@id="imageGallery"][1]/li/@data-src').extract()
        print image_gallerys



