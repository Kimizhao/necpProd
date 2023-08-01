FROM continuumio/miniconda3

WORKDIR /opt/necpProd
COPY . .

# 安装cron
RUN apt-get update && apt-get install -y cron

# 安装scrapy和aria2p依赖
RUN conda install -c conda-forge scrapy aria2p

# 将 crontab 文件复制到容器的 cron 目录中
COPY crontab /etc/cron.d/my-cron-job

# 给 crontab 文件添加可执行权限 新增任务
RUN chmod 0644 /etc/cron.d/my-cron-job && crontab /etc/cron.d/my-cron-job

# 创建日志文件以收集 cron 任务的输出
RUN touch /var/log/cron.log

# 启动cron
CMD ["/bin/bash"]