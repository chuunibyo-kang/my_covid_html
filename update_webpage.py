import time
from map_build import mainland_all_city_data_map, risk_area_map


#用于更新网页
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