# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    baseURL = "https://hr.tencent.com/position.php?&start="
    offset = 0
    start_urls = [baseURL + str(offset)]


    def parse(self, response):
        node_list = response.xpath('//tr[@class="odd"]|//tr[@class="even"]')
        for node in node_list:
            item = TencentItem()
            item['position_name'] = node.xpath('./td[1]/a/text()').extract()[0]
            item['position_link'] = node.xpath('./td[1]/a/@href').extract()[0]
            if len(node.xpath('./td[2]/text()')):
                item['position_type'] = node.xpath('./td[2]/text()').extract()[0]
            else:
                item['position_type'] =" "
            item['position_num'] = node.xpath('./td[3]/text()').extract()[0]
            item['workplace'] = node.xpath('./td[4]/text()').extract()[0]
            item['publishtime'] = node.xpath('./td[5]/text()').extract()[0]

            yield item

        if self.offset < 500:
            self.offset += 10
            url = self.baseURL + str(self.offset)
            yield scrapy.Request(url,callback = self.parse)


