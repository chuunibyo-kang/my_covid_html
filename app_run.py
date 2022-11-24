#导入flask框架模块
from flask import Flask,render_template,request

import requests

from config import PORT

from map_build import *

#导入写好的查询模块和爬虫模块
from get_data import *
from crawler import *

#获取IP
app = Flask(__name__, static_folder = "static",template_folder = "templates")

#获取本土数据，把数据类型转换成列表类型
#对“新增”的数据加上“+”号
def pass_mainland_data():
    mainland_data = list(get_mainland_data())
    for i in range(len(mainland_data)):
        if i > 0:
            mainland_data[i] = "+"+str(mainland_data[i])
    return mainland_data

#获取整体数据，把数据类型转换成列表类型
#对“新增”的数据加上“+”号
def pass_whole_data():
    whole_data = list(get_whole_data())
    for i in range(len(whole_data)):
        if i > 1:
            whole_data[i] = "+"+str(whole_data[i])
    return whole_data

#更新日期
def update_date():
    date = get_data_update_date()
    return date

#路由部分，多数用于返回疫情数据

@app.route("/")
def index():
    return render_template(
            'index.html',
            mainland_data = pass_mainland_data(),
            whole_data = pass_whole_data(),
            update_date = update_date(),
            )

# 用于网页更新疫情数据，HTML内有按钮能调用这个爬虫函数
# 这个return值随便写的，因为暂时不需要啥返回值
@app.route("/click_update_data")
def click_update_data():
    crawler_run()
    return "更新成功"


# 初始化可视化地图，并将图的数据转化为json，用于html页面调用echarts再次生成
# 这样做能让也面生成更灵活
@app.route("/visual_map")
def visual_map():
    map = visual_data_map()
    return map.dump_options_with_quotes()

# 初始化近期整体趋势折线图，并将图的数据转化为json，用于html页面调用echarts再次生成
@app.route("/current_overall_line_map")
def recent_overall_line_map():
    overall_line_map =  recent_overall_data_line_map()
    return overall_line_map.dump_options_with_quotes()

# 初始化近期新增数据折线图，并将图的数据转化为json，用于html页面调用echarts再次生成
@app.route("/current_daily_line_map")
def recent_daily_line_map():
    daily_line_map = recent_daily_data_line_map()
    return daily_line_map.dump_options_with_quotes()

# 初始化累计确诊TOP5柱状图，并将图的数据转化为json，用于html页面调用echarts再次生成
@app.route("/total_confirm_top5_data_map")
def total_confirm_top5_map():
    total_bar_map = total_confirm_top5_data_map()
    return total_bar_map.dump_options_with_quotes()

# 初始化新增确诊TOP5柱状图，并将图的数据转化为json，用于html页面调用echarts再次生成
@app.route("/today_confirm_add_top5_data_map")
def today_confirm_add_top5_map():
    today_bar_map = today_confirm_add_top5_data_map()
    return today_bar_map.dump_options_with_quotes()

if __name__ == "__main__":
    #如果想单独看网页数据，可以用build_charts_html的方法
    # build_charts_html()
    app.run(
            host="0.0.0.0"
            ,port = PORT
            ,debug = True
            )


