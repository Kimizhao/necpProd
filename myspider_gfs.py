#!/opt/conda/envs/python3715/bin/python
# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
import scrapy
import aria2p

# initialization, these are the default values
aria2 = aria2p.API(
    aria2p.Client(
        host="http://192.168.165.68",
        # host="http://localhost",
        port=6800,
        secret="P3TERX"
    )
)


def filter_links(link):
    if 'Parent Directory' in link:
        return False
    return True


class MySpider(scrapy.Spider):
    name = 'myspider_gfs'

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.date_hour = kwargs.get('date_hour')
        # 判断date_hour属性，如果该属性不为空则使用date_hour参数，否则使用当前时间
        # 例如：scrapy crawl myspider_gfs -a date_hour=2023070300
        if self.date_hour is not None:
            # 获取当前UTC时间
            current_time = datetime.strptime(self.date_hour, '%Y%m%d%H')
        else:
            current_time = datetime.utcnow()

        # 计算前2小时的时间
        two_hours_ago = current_time - timedelta(hours=2)

        # 获取当前UTC日期，格式为：20230703
        date = two_hours_ago.strftime('%Y%m%d')
        # 当前时间所处的时段，间隔为6小时
        hour = int(two_hours_ago.strftime('%H'))
        if 0 <= hour < 6:
            aa = '00'
        elif 6 <= hour < 12:
            aa = '06'
        elif 12 <= hour < 18:
            aa = '12'
        elif 18 <= hour < 24:
            aa = '18'

        gfs_url = f'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{aa}/'

        # start_urls = ['https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20230703/00/']
        self.start_urls = [gfs_url]

        self.count = 1

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 在这里解析响应并提取链接
        # 使用XPath选择所有链接元素，然后使用extract()方法提取过滤链接
        links = response.xpath('//a/@href').getall()

        links = links[1:]

        for link in links:
            # 非目录链接
            if not link.endswith('/'):
                # print('文件名: ', link)
                # print('文件链接: ', response.url)
                url = response.urljoin(link)
                print('文件下载链接: ', url)

                # 判断是否是grib2结尾的文件
                if link.endswith('grib2') is False:
                    continue

                # 每100个文件休眠300秒
                if self.count % 100 == 0:
                    time.sleep(300)

                directory = response.url.replace('https://', '/downloads/')
                print('文件保存目录: ', directory)

                options = {"dir": directory}
                aria2.add(url, options=options)

                # 休眠1秒
                time.sleep(1)
                self.count = self.count + 1

            else:
                if link.startswith('enkfgdas.') is False and link.startswith('gdas.') is False and link.startswith('bufr.') is False and link.startswith('station/') is False and link.startswith('atmos/') is False:
                    print('目录链接: ', link)
                    yield scrapy.Request(url=response.urljoin(link), callback=self.parse)

        # 处理子链接
        # 如果要限制爬取的深度，可以增加一个参数来跟踪当前的深度，并在适当时停止递归调用
        # 例如：yield scrapy.Request(url=response.urljoin(link), callback=self.parse, meta={'depth': depth + 1})
