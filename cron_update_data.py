# 用于服务端crontab定期运行爬虫函数
import time
from crawler import crawler_run
from map_build import mainland_all_city_data_map, risk_area_map

#运行爬虫程序
crawler_run()

#更新风险地区网页
print(f'{time.asctime()} 正在更新风险地区网页')
if risk_area_map():
    print(f"{time.asctime()} 风险地区网页更新完毕")
else:
    print(f"{time.asctime()} 风险地区网页更新失败")

#更新本土省份疫情数据网页
print(f"{time.asctime()} 正在更新本土省疫情数据网页")
if mainland_all_city_data_map():
    print(f"{time.asctime()} 本土省疫情数据网页更新完毕")
else:
    print(f"{time.asctime()} 本土省疫情数据网页更新失败")

print('''--------------更新完毕----------------------
''')