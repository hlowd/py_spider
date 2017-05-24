import scrapy
import scpy.items as it

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "https://www.baidu.com"
    ]

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        item = it.baiduItem()
        item['title'] =sel.xpath('//title/text()')[0].extract()
        yield item
