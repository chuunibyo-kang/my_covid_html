#导入pyecharts模块
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import Map,Bar,Line,PictorialBar
from pyecharts import options as opts
from pyecharts.globals import SymbolType

#导入写好的查询模块和爬虫模块
from get_data import *
from crawler import *


#生成每日新增确诊可视化地图
def visual_confirm_add_data_map():
    #data获取到的数据是(省份，人数)，直接导入到map方法里可以直接使用，无需处理
    data = get_province_confirm_add_data()
    map = (
    Map(init_opts=opts.InitOpts(chart_id='China_confirm_add_data_visual_map'))
    .add("新增确诊",data, "china",is_roam=False)
    .set_global_opts(
        title_opts=opts.TitleOpts(title=" 全国每日新增确诊可视化地图（无澳门数据）",pos_left="center", pos_top="10%"),
        visualmap_opts=opts.VisualMapOpts(
            is_show = False,
            range_color = ['#ffffff','#ffe4d9','#ff907c','#ff665a','#fb1b30','#ca0000'],
                            max_ = 100),
            legend_opts = opts.LegendOpts(is_show = False))
    ) 
    return map

#生成每日新增无症状可视化地图
def visual_asymptomatic_add_data_map():
    #data获取到的数据是(省份，人数)，直接导入到map方法里可以直接使用，无需处理
    data = get_province_asymptomatic_add_data()
    map = (
    Map(init_opts=opts.InitOpts(chart_id='China_asymptomatic_add_data_visual_map'))
    .add("新增无症状",data, "china",is_roam=False)
    .set_global_opts(
        title_opts=opts.TitleOpts(title=" 全国每日新增无症状可视化地图（无港澳台数据）",pos_left="center", pos_top="10%"),
        visualmap_opts=opts.VisualMapOpts(
            is_show = False,
            range_color = ['#ffffff','#ffe4d9','#ff907c','#ff665a','#fb1b30','#ca0000'],
                            max_ = 200),
            legend_opts = opts.LegendOpts(is_show = False))
    ) 
    return map    

#生成最近7天每日总体趋势折线图
# def recent_overall_data_line_map() -> Line:
#     data = get_recent_overall_data()
#     date_list = [i[0].strftime('%Y-%m-%d') for i in data]
#     confirm_list= [i[1] for i in data]
#     line_map =(
#     Line(init_opts=opts.InitOpts(chart_id='current_overall_data_line_map'))
#         .add_xaxis([i for i in date_list])
#         .add_yaxis("累计确诊",[i for i in confirm_list])
#     .set_global_opts(title_opts=opts.TitleOpts(title="近期全国累计数据趋势（包含港澳台）"))
#     )
#     return line_map

#生成最近7天每日总体趋势折线图
def recent_overall_data_line_map() -> PictorialBar:
    data = get_recent_overall_data()
    date_list = [i[0].strftime('%Y-%m-%d') for i in data]
    confirm_list= [i[1] for i in data]
    bar_map =(
    PictorialBar(init_opts=opts.InitOpts(chart_id='current_overall_data_line_map'))
        .add_xaxis(date_list)
        .add_yaxis("累计确诊",confirm_list,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=20,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol=SymbolType.ROUND_RECT)
    .set_global_opts(title_opts=opts.TitleOpts(title="近期全国累计数据趋势（包含港澳台）"))
    ).reversal_axis()
    return bar_map

#生成最近7天全国每日新增确诊趋势折线图
def recent_daily_confirm_add_data_line_map() -> Line:
    data = get_recent_daily_confirm_add_data()
    date_list = [i[0].strftime('%Y-%m-%d') for i in data]
    confirm_add_list= [i[1] for i in data]
    line_map =(
    Line(init_opts=opts.InitOpts(chart_id='current_add_data_line_map'))
        .add_xaxis([i for i in date_list])
        .add_yaxis("全国新增确诊",[i for i in confirm_add_list])
    .set_global_opts(title_opts=opts.TitleOpts(title="近期全国新增确诊趋势（包含港澳台）"))
    )
    return line_map

#生成最近7天本土每日新增确诊趋势折线图
def recent_mainland_daily_confirm_add_data_line_map() -> Line:
    data = get_recent_mainland_daily_confirm_add_data()
    date_list = [i[0] for i in data]
    confirm_add_list= [i[1] for i in data]
    line_map =(
    Line(init_opts=opts.InitOpts(chart_id='current_add_data_line_map'))
        .add_xaxis([i for i in date_list])
        .add_yaxis("本土新增确诊",[i for i in confirm_add_list])
        
    .set_global_opts(title_opts=opts.TitleOpts(title="近期本土新增确诊趋势（不包含港澳台）"))
    )
    return line_map

#生成最近7天本土每日新增无症状趋势折线图
def recent_mainland_daily_asymptomatic_add_data_map() -> Line:
    data = get_recent_mainland_daily_asymptomatic_add_data()
    date_list = [i[0] for i in data]
    confirm_add_list= [i[1] for i in data]
    line_map =(
    Line(init_opts=opts.InitOpts(chart_id='current_add_data_line_map'))
        .add_xaxis([i for i in date_list])
        .add_yaxis("本土新增无症状",[i for i in confirm_add_list])
        
    .set_global_opts(title_opts=opts.TitleOpts(title="近期本土新增无症状趋势（不包含港澳台）"))
    )
    return line_map

#生成累计确诊top5柱状图
def total_confirm_top5_data_map() -> Bar:
    data = get_total_confirm_top5_data()
    province = [i[0] for i in data]
    confirm_number = [i[1] for i in data]
    bar_map = (
    Bar(init_opts=opts.InitOpts(chart_id='total_confirm_top5_data_map'))
    .add_xaxis(province)
    .add_yaxis("累计确诊人数",confirm_number)
    .set_global_opts(title_opts=opts.TitleOpts(title="全国累计确诊省份TOP5"))
    )
    return bar_map

#生成累计确诊top5柱状图（不包含港澳台）
def total_confirm_top5_mainland_data_map() -> Bar:
    data = get_total_confirm_top5_mainland_data()
    province = [i[0] for i in data]
    confirm_number = [i[1] for i in data]
    bar_map = (
    Bar(init_opts=opts.InitOpts(chart_id='total_confirm_top5_mainland_data_map'))
    .add_xaxis(province)
    .add_yaxis("累计确诊人数",confirm_number)
    .set_global_opts(title_opts=opts.TitleOpts(title="全国累计确诊省份TOP5(不包含港澳台)"))
    )
    return bar_map   

#生成新增确诊top5柱状图
def today_confirm_add_top5_data_map() -> Bar:
    data = get_today_confirm_add_top5_data()
    province = [i[0] for i in data]
    confirm_add_number = [i[1] for i in data]
    bar_map = (
    Bar(init_opts=opts.InitOpts(chart_id='today_confirm_add_top5_data_map'))
    .add_xaxis(province)
    .add_yaxis("新增确诊人数", confirm_add_number)
    .set_global_opts(title_opts=opts.TitleOpts(title="全国今日新增确诊省份TOP5"))
    )
    return bar_map

#生成新增确诊top5柱状图(不包含港澳台)
def today_confirm_add_top5_mainland_data_map() -> Bar:
    data = get_today_confirm_add_top5_mainland_data()
    province = [i[0] for i in data]
    confirm_add_number = [i[1] for i in data]
    bar_map = (
    Bar(init_opts=opts.InitOpts(chart_id='today_confirm_add_top5_mainland_data_map'))
    .add_xaxis(province)
    .add_yaxis("新增确诊人数", confirm_add_number)
    .set_global_opts(title_opts=opts.TitleOpts(title="全国今日新增确诊省份TOP5(不包含港澳台)"))
    )
    return bar_map    

#生成风险地区数据
def risk_area_map():
    risk_table = Table()
    headers = ["风险","省", "市", "区/县/街道", "社区",]
    rows = [i for i in get_risk_area_date()]
    risk_table = risk_table.add(headers, rows)
    risk_table.set_global_opts(
            title_opts=ComponentTitleOpts(title="", subtitle=""))
    return risk_table.render("templates/risk_table.html")

# 将数据图表生成独立的网页文件，有需要可以使用
# def build_charts_html():
#     visual_data_map().render("my_covid_html/templates/visual_data_map.html")
#     five_days_overall_data_line_map().render("my_covid_html/templates/five_days_overall_data_line_map.html")
#     five_days_daily_data_line_map().render("my_covid_html/templates/five_days_daily_data_line_map.html")
#     total_confirm_top5_data_map().render("my_covid_html/templates/total_confirm_top5_data_map.html")
#     today_confirm_add_top5_data_map().render("my_covid_html/templates/today_confirm_add_top5_data_map.html")


#如果只想就在一个页面生成“仪表盘式”的页面，可以用page方法生成
#先去origin_index网页设置好网页布局，然后保存json表，使用save_resize_html方法调整

# def build_page_html():
#     page = Page(page_title= "疫情数据可视化",layout=Page.DraggablePageLayout)
#     page.add(
#         visual_data_map(),
#         five_days_overall_data_line_map(),
#         five_days_daily_data_line_map(),
#         total_confirm_top5_data_map(),
#         today_confirm_add_top5_data_map(),
#     )
#     page.render('/root/my_covid_html/templates/origin_page.html')

#     Page.save_resize_html(
# 	source="/root/my_covid_html/templates/origin_page.html",
# 	cfg_file="/root/my_covid_html/templates/chart_config.json",
# 	dest="/root/my_covid_html/templates/resize_page.html"
#     )
#     return page
#
#
# @app.route("/")
# def index():
#     return render_template('index.html')

