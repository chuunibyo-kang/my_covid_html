# 执行cron_update这个python程序，而这个shell文件会被crontab执行

#!/bin/bash

/etc/init.d/mysql restart

cd /root/my_covid_html

/bin/python cron_update_data.py >> /root/crawler_run.log
