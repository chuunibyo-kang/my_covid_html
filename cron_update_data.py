# 用于服务端crontab定期运行爬虫函数
import time
from crawler import crawler_run
from map_build import risk_area_map,mainland_all_province_data_map


crawler_run()
print(f'{time.asctime()} 正在更新风险地区网页')
if risk_area_map():
    print(f"{time.asctime()} 风险地区网页更新完毕")
else:
    print(f"{time.asctime()} 风险地区网页更新失败")


print(f"{time.asctime()} 正在更新本土省疫情数据网页")
if mainland_all_province_data_map():
    print(f"{time.asctime()} 本土省疫情数据网页更新完毕")
else:
    print(f"{time.asctime()} 本土省疫情数据网页更新失败")

print("--------------更新完毕----------------------")
