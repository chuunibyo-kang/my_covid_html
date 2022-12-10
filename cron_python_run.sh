# 执行cron_update这个python程序，而这个shell文件会被crontab执行
#!/bin/bash

/etc/init.d/mysql restart

cd /root

/bin/python my_covid_html/cron_update_data.py >> crawler_run.log
