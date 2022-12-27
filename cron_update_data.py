# 用于服务端crontab定期运行爬虫函数
from crawler import crawler_run
from map_build import mainland_all_city_data_map, risk_area_map

#运行爬虫程序
crawler_run()

print('''--------------更新完毕----------------------
''')