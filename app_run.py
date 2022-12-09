#导入flask框架模块
from flask import Flask,render_template,request

from config import PORT

from map_build import *

#导入写好的查询模块和爬虫模块
from get_data import *
from crawler import *

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

#服务器更新日期
def update_date():
    date = get_data_update_date()
    return date

#设置首页路由，传入的数据包括本土数据、整体数据、服务器更新数据时间
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
    risk_area_map()
    return "更新成功"

#设置整体疫情数据表网页路由，传入的数据包括本土数据、整体数据、服务器更新数据时间
@app.route("/covid_information_table")
def covid_information_table():
    return render_template(
            'covid_information_table.html',
            mainland_data = pass_mainland_data(),
            whole_data = pass_whole_data(),
            update_date = update_date(),
            )


#设置可视化疫情数据地图数据路由
#这个路由传输的是数据，用于网页内的ajax生成图表数据的请求
@app.route("/visual_confirm_add_data_map_data")
def visual_confirm_add_map_data():
    map = visual_confirm_add_data_map()
    return map.dump_options_with_quotes()

@app.route("/visual_asymptomatic_add_data_map_data")
def visual_asymptomatic_add_map_data():
    map = visual_asymptomatic_add_data_map()
    return map.dump_options_with_quotes()

#设置可视化疫情数据地图网页路由
@app.route("/visual_China_map")
def visual_map():
    return render_template(
            'visual_China_map.html',
            mainland_data = pass_mainland_data(),
            whole_data = pass_whole_data(),
            update_date = update_date(),
            )

#设置近期整体趋势折线图json数据路由
#这个路由传输的是数据，用于网页内的ajax生成图表数据的请求
# 初始化近期整体趋势折线图，并将图的数据转化为json，用于html页面调用echarts再次生成
@app.route("/current_overall_line_map_data")
def current_overall_line_map_data_data():
    overall_line_map =  recent_overall_data_line_map()
    return overall_line_map.dump_options_with_quotes()
#设置近期整体趋势折线图网页路由
@app.route("/current_overall_line_map")
def rcurrent_overall_line_map():
    return render_template(
            'current_overall_line_map.html',
            mainland_data = pass_mainland_data(),
            whole_data = pass_whole_data(),
            update_date = update_date(),
            )

#设置近期新增数据折线图json数据路由
#这个路由传输的是数据，用于网页内的ajax生成图表数据的请求
# 初始化近期新增数据折线图，并将图的数据转化为json，用于html页面调用echarts再次生成
@app.route("/current_daily_confirm_add_data_line_map_data")
def current_daily_confirm_add_line_map_data():
    daily_line_map = recent_daily_confirm_add_data_line_map()
    return daily_line_map.dump_options_with_quotes()

@app.route("/current_daily_mainland_confirm_add_data_line_map_data")
def current_daily_mainland_confirm_add_line_map_data():
    daily_line_map = recent_mainland_daily_confirm_add_data_line_map()
    return daily_line_map.dump_options_with_quotes()

@app.route("/current_daily_mainland_asymptomatic_add_data_line_map_data")
def current_daily_mainland_asymptomatic_add_line_map_data():
    daily_line_map = recent_mainland_daily_asymptomatic_add_data_map()
    return daily_line_map.dump_options_with_quotes()

#设置近期新增数据折线图网页路由
@app.route("/current_daily_line_map")
def current_daily_line_map():
    return render_template(
            'current_daily_line_map.html',
            mainland_data = pass_mainland_data(),
            whole_data = pass_whole_data(),
            update_date = update_date(),
            )

#设置累计确诊TOP5柱状图数据json数据路由
#这个路由传输的是数据，用于网页内的ajax生成图表数据的请求
# 初始化累计确诊TOP5柱状图，并将图的数据转化为json，用于html页面调用echarts再次生成
@app.route("/total_confirm_top5_data_map_data")
def total_confirm_top5_map_data():
    total_bar_map = total_confirm_top5_data_map()
    return total_bar_map.dump_options_with_quotes()

@app.route("/total_confirm_top5_mainland_data_map_data")
def total_confirm_top5_map_mainland_data():
    total_bar_map = total_confirm_top5_mainland_data_map()
    return total_bar_map.dump_options_with_quotes()

#设置累计确诊TOP5柱状图网页路由
@app.route("/total_confirm_top5_data_map")
def total_confirm_top5_map():
    return render_template(
            'total_confirm_top5_data_map.html',
            mainland_data = pass_mainland_data(),
            whole_data = pass_whole_data(),
            update_date = update_date(),
            )

#设置新增确诊TOP5柱状图数据json数据路由
#这个路由传输的是数据，用于网页内的ajax生成图表数据的请求
# 初始化新增确诊TOP5柱状图，并将图的数据转化为json，用于html页面调用echarts再次生成
@app.route("/today_confirm_add_top5_data_map_data")
def today_confirm_add_top5_map_data():
    today_bar_map = today_confirm_add_top5_data_map()
    return today_bar_map.dump_options_with_quotes()

@app.route("/today_confirm_add_top5_mainland_data_map_data")
def today_confirm_add_top5_map_mainland_data():
    today_bar_map = today_confirm_add_top5_mainland_data_map()
    return today_bar_map.dump_options_with_quotes()

#设置新增确诊TOP5柱状图网页路由
@app.route("/today_confirm_add_top5_data_map")
def today_confirm_add_top5_map():
    return render_template(
            'today_confirm_add_top5_data_map.html',
            mainland_data = pass_mainland_data(),
            whole_data = pass_whole_data(),
            update_date = update_date(),
            )

#设置风险地区网页路由
@app.route("/risk_area", methods=['GET', 'POST'])
def get_select_tag_data():
    # if request.method == 'POST':
    #     risk_province = request.form.get('province')
    #     risk_level = request.form.get('risk_level')
    #     risk_area_map(risk_province,risk_level)
    return render_template(
        'risk_area.html',
        risk_area_update_date = get_risk_area_update_date(),
        update_date = update_date(),
        high_risk_area_number = get_high_risk_area_number(),
        low_risk_area_number = get_low_risk_area_number()
    # ,province = get_province_list()
    )

#设置风险地区详细版网页路由
@app.route("/risk_area_data")
def risk_area_search_data():
    return render_template('risk_table.html')

if __name__ == "__main__":
    #如果想单独看网页数据，可以用build_charts_html的方法
    # build_charts_html()
    risk_area_map = risk_area_map()
    app.run(
        #这里的IP最好是设置成本机的IP
            host="0.0.0.0"
            ,port = PORT
            ,debug = True
            )
