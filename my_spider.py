import scrapy

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['http://example.com']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 使用XPath选择所有链接元素
        links = response.xpath('//a/@href').getall()

        for link in links:
            if link.endswith('.nc'):
                # 处理满足条件的链接
                yield {
                    'url': link,
                    'other_info': '...'
                }

            # 发送请求或执行其他操作
            # yield scrapy.Request(url=link, callback=self.parse_other_page)
