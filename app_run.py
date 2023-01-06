#导入flask框架模块
from flask import Flask,render_template,request

from config import PORT

from map_build import *

#导入写好的查询模块和爬虫模块
from get_data import *
from crawler import *

app = Flask(__name__, static_folder = "static",template_folder = "templates")


#设置首页路由，
@app.route("/")
def index():
    if 'Android' in str(request.user_agent):
        return render_template("moblie_index.html",update_date = get_data_update_date())
    else:
        return render_template("index.html",update_date = get_data_update_date())

#设置整体疫情数据表网页路由
#传入的数据包括疫情新增数据、本土数据、整体累计数据、今日与昨日整体累计差异数据
#和服务器更新数据时间
@app.route("/covid_information_table")
def covid_information_table():
    if 'Android' in str(request.user_agent):
        return render_template(
            "moblie_covid_information_table.html",
            newly_added_data = get_newly_added_data(),
            overall_data = get_overall_data(),
            overall_gap_data = get_overall_gap_data(),
            update_date = get_data_update_date())
    else:
        return render_template(
            'covid_information_table.html',
            newly_added_data = get_newly_added_data(),
            overall_data = get_overall_data(),
            overall_gap_data = get_overall_gap_data(),
            update_date = get_data_update_date(),
            )

#本土省份的疫情数据路由
@app.route("/mainland_all_city_data_map")
def mainland_all_city_data_map_data():
    return render_template('mainland_all_city_data_map.html')

#设置可视化新增确诊地图数据路由
#这个路由传输的是数据，用于网页内的ajax生成图表数据的请求
@app.route("/visual_confirm_add_data_map_data")
def visual_confirm_add_map_data():
    map = visual_confirm_add_data_map()
    return map.dump_options_with_quotes()

#设置可视化新增确诊地图数据路由
#这个路由传输的是数据，用于网页内的ajax生成图表数据的请求
@app.route("/visual_confirm_now_data_map_data")
def visual_confirm_now_map_data():
    map = visual_confirm_now_data_map()
    return map.dump_options_with_quotes()

#设置可视化疫情数据地图网页路由
@app.route("/visual_China_map")
def visual_map():
    if 'Android' in str(request.user_agent):
        return render_template("moblie_visual_China_map.html",update_date = get_data_update_date())
    else:
        return render_template("visual_China_map.html",update_date = get_data_update_date())

#设置全国/本土近期累计确诊趋势图json数据路由
#这个路由传输的是数据，用于网页内的ajax生成图表数据的请求
# 初始化近期整体趋势折线图，并将图的数据转化为json，用于html页面调用echarts再次生成
@app.route("/current_overall_confirm_bar_map_data")
def current_overall_confirm_bar_map_data():
    overall_bar_map =  recent_overall_confirm_data_bar_map()
    return overall_bar_map.dump_options_with_quotes()

@app.route("/current_mainland_overall_confirm_line_map_data")
def current_mainland_overall_confirm_bar_map_data():
    overall_line_map =  recent_mainland_overall_confirm_data_line_map()
    return overall_line_map.dump_options_with_quotes()
    
#设置近期整体趋势折线图网页路由
@app.route("/current_overall_confirm_line_map")
def rcurrent_overall_line_map():
    if 'Android' in str(request.user_agent):
        return render_template(
            "moblie_current_overall_line_map.html",
            update_date = get_data_update_date())
    else:
        return render_template(
            'current_overall_line_map.html',
            update_date = get_data_update_date(),
            )

#设置近期新增数据折线图json数据路由
#第一个是近期全国新增确诊、第二个是近期本土新增确诊、第三个是近期本土无症状新增
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

#设置近期新增数据折线图网页路由
@app.route("/current_daily_line_map")
def current_daily_line_map():
    if 'Android' in str(request.user_agent):
        return render_template(
            "moblie_current_daily_line_map.html",
            update_date = get_data_update_date())
    else:
        return render_template(
            'current_daily_line_map.html',
            update_date = get_data_update_date()
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

# #设置累计确诊TOP5柱状图网页路由
# @app.route("/total_confirm_top5_data_map")
# def total_confirm_top5_map():
#     return render_template(
#             'total_confirm_top5_data_map.html',
#             mainland_data = pass_mainland_data(),
#             whole_data = pass_whole_data(),
#             update_date = get_data_update_date(),
#             )

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

#设置省份数据TOP5柱状图网页路由
@app.route("/province_top5_data_map")
def confirm_top5_map():
    if 'Android' in str(request.user_agent):
        return render_template("moblie_province_top5_data_map.html",
        update_date = get_data_update_date())
    else:
        return render_template(
            'province_top5_data_map.html',
            update_date = get_data_update_date()
            )

#设置风险地区网页路由
@app.route("/risk_area", 
# methods=['GET', 'POST']
)
def get_select_tag_data():
    # if request.method == 'POST':
    #     risk_province = request.form.get('province')
    #     risk_level = request.form.get('risk_level')
    #     risk_area_map(risk_province,risk_level)
    if 'Android' in str(request.user_agent):
        return render_template("moblie_risk_area.html",
        update_date = get_data_update_date(),
        high_risk_area_number = get_high_risk_area_number(),
        low_risk_area_number = get_low_risk_area_number()
        )
    else:
        return render_template(
        'risk_area.html',
        risk_area_update_date = get_risk_area_update_date(),
        update_date = get_data_update_date(),
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
    app.run(
        #这里的IP最好是设置成本机的IP
            host="0.0.0.0"
            ,port = PORT
            ,debug=True
            )
