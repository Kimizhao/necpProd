import requests
import json
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
import time
from datetime import datetime, timedelta
import aria2p
import re

downloads_path = "/downloads/GFS"

# initialization, these are the default values
aria2 = aria2p.API(
    aria2p.Client(
        host="http://192.168.165.78",
        # host="http://localhost",
        port=6801,
        secret="P3TERX",
        timeout=300
    )
)

# 初始化日志
def initlog():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='log.log',
        filemode='a',
    )

    logging.getLogger('').addHandler(TimedRotatingFileHandler('log.log', 'midnight', interval=1
                                                              , backupCount=7))
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def download_gfs(date_hour):
    # 捕获异常
    try:
        # 读取json文件
        with open('gfs_forecasts.json', 'r') as json_file:
            data = json.load(json_file)

        # data中parameters和levels是数组，需要转换成字符串，以&分隔
        parameters = '&'.join(data['parameters'])
        levels = '&'.join(data['levels'])

        if date_hour is not None:
            # 获取当前UTC时间
            current_time = datetime.strptime(date_hour, '%Y%m%d%H')
            # 计算前2小时的时间
            download_hour = current_time
        else:
            current_time = datetime.utcnow()
            # 计算前2小时的时间
            download_hour = current_time - timedelta(hours=1)

        logging.info(f"download_hour: {download_hour}")

        # 获取当前UTC日期，格式为：20230703
        date = download_hour.strftime('%Y%m%d')
        # 当前时间所处的时段，间隔为6小时
        hour = int(download_hour.strftime('%H'))
        if 0 <= hour < 6:
            cycle = '00'
        elif 6 <= hour < 12:
            cycle = '06'
        elif 12 <= hour < 18:
            cycle = '12'
        elif 18 <= hour < 24:
            cycle = '18'

        count = 1

        # 批量生成url，根据date、cycle、f
        # FFF is the forecast hour of product from 000 - 120 step 1, 123 - 384 step 3，放在一个列表中
        forecast_list = []
        for f in range(0, 120, 1):
            forecast_list.append(f)

        for f in range(120, 384 + 1, 3):
            forecast_list.append(f)

        # 遍历forecast_list，生成url
        for f in forecast_list:
            # 拼接directory
            # directory = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{cycle}/atmos"
            directory = f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{f:03d}"
            # 拼接文件名
            filename = f"gfs.{date}.t{cycle}z.pgrb2.0p25.f{f:03d}.grib2"

            # 拼接url
            url = f"{directory}&{parameters}&{levels}"

            out_directory = f"{downloads_path}/nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{cycle}/atmos/filter"

            # options = {"dir": out_directory, "out": filename}
            # 覆盖已存在的文件
            # options = {"dir": out_directory, "out": filename, "allow-overwrite": "true"}
            options = {"dir": out_directory, "out": filename, "allow-overwrite": "true"}
            dirs = aria2.add(url, options=options)
            logging.info(f'文件保存目录: {out_directory}/{filename}')

            # 每100个文件休眠300秒
            # if count % 100 == 0:
            #     time.sleep(300)

            # 休眠1秒
            time.sleep(4)
            count += 1

            # filename = "gfs_data.grib2"
            # response = requests.get(url)
            #
            # if response.status_code == 200:
            #     with open(out_directory, 'wb') as file:
            #         file.write(response.content)
            #         print(f"File downloaded successfully: {out_directory}")
            # else:
            #     print("Failed to download the file")

    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    initlog()
    # 判断是否有参数
    if len(sys.argv) > 1:
        date_hour = sys.argv[1]
        download_gfs(date_hour)
    else:
        download_gfs(None)
