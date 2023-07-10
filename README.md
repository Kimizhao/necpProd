# necpProd

## 抓取地址：
https://nomads.ncep.noaa.gov/


## 安装依赖包
```shell
conda install -c conda-forge scrapy
conda install -c conda-forge aria2p
```

## 参考
[scrapy](https://scrapy.org/)
[Aria2-Pro-Docker](https://github.com/P3TERX/Aria2-Pro-Docker)


## 定时任务
```shell
crontab -e
```
```shell
0 6,12,18,0 * * * cd /opt/ecdata/necpProd;/opt/conda/envs/python3715/bin/scrapy runspider myspider_gfs.py >> /var/log/myspider_gfs.log 2>&1
0 7 * * * cd /opt/ecdata/necpProd;/opt/conda/envs/python3715/bin/scrapy runspider myspider_nsst.py >> /var/log/myspider_nsst.log 2>&1
```

## 说明
新增参数
```shell
scrapy runspider myspider_gfs.py -a date_hour=2023070300
