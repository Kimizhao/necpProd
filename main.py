from scrapy.cmdline import execute
import os
import sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # execute(['scrapy', 'runspider', 'myspider_nsst.py'])
    execute(['scrapy', 'runspider', 'myspider_gfs.py', '-a', 'date_hour=2023072500'])
    # execute(['scrapy', 'runspider', 'myspider_psurge.py', '-a', 'date_hour=20230707'])