#这个文件用于查询已经在数据库中的数据
#查询出来的数据用于网页中

import pymysql

from config import *

#连接数据库
def get_database():
    db = pymysql.connect(
        host=HOST, 
        user=USER, 
        password=PASSWORD, 
        database=DATABASE)
    if db.open:
        cursor = db.cursor()
        return db, cursor
    else:
        raise Exception('数据库连接失败')

#关闭数据库
def close_database(db, cursor):
    cursor.close()
    db.close()

#执行数据库查询的函数
#每一次查询都要执行以下的步骤：
#连接数据库、打开游标、执行语句、抓取结果、关闭数据库、返回抓取结果
def query(sql:str):
    db, cursor = get_database()
    cursor.execute(sql)
    result = cursor.fetchall()
    close_database(db, cursor)  
    return result

#获取国内的整体数据
#包括最新一天的确诊总人数、今日新增、累计治愈、今日治愈、累计死亡，今日死亡
def get_whole_data() -> tuple:
    select_sql = """
    SELECT confirm, heal, confirm_add
    FROM history_data 
    ORDER BY update_date DESC 
    LIMIT 1
    """
    return query(select_sql)[0]


#获取国内的本土数据
#包括最新一天的本土现有确诊人数、本土新增确诊、本土现有无症状、本土新增无症状
def get_mainland_data():
    select_sql = """
    SELECT mainland_confirm_now,mainland_confirm_add,mainland_asymptomatic_add
    FROM mainland_data 
    ORDER BY update_date DESC 
    LIMIT 1
    """
    return query(select_sql)[0]


#获取每个省的每日新增确诊人数，用于中国地图可视化地图
def get_province_confirm_add_data():
    select_sql = """
    SELECT province,SUM(confirm_add) 
    FROM details_data
    WHERE update_date=
        (SELECT update_date
        FROM details_data 
        ORDER BY update_date DESC 
        LIMIT 1)
    GROUP BY province
    """
    return query(select_sql)

##获取每个省的每日新增无症状人数，用于中国地图可视化地图
def get_province_asymptomatic_add_data():
    select_sql = """
    SELECT province,SUM(asymptomatic_add) 
    FROM details_data
    WHERE update_date=
        (SELECT update_date
        FROM details_data 
        ORDER BY update_date DESC 
        LIMIT 1)
    GROUP BY province
    """
    return query(select_sql)

# 获取最近7天全国整体趋势数据
# 包括更新时间、累计确诊、累计治愈、累计死亡
def get_recent_overall_data():
    select_sql = """
    SELECT result.update_date, result.confirm
    FROM (
    (
    SELECT update_date,confirm
    FROM history_data
    ORDER BY update_date DESC 
    LIMIT 7
    ) AS result
    )
    ORDER BY result.update_date 
    """
    return query(select_sql)

# 获取最近7天全国每日新增数据
# 包括更新时间、新增确诊
def get_recent_daily_confirm_add_data():
    select_sql = """
    SELECT result.update_date, result.confirm_add
    FROM (
    (
    SELECT update_date,confirm_add
    FROM history_data
    ORDER BY update_date DESC 
    LIMIT 7
    ) AS result
    )
    ORDER BY result.update_date 
    """
    return query(select_sql)

# 获取最近7天本土每日新增确诊数据
def get_recent_mainland_daily_confirm_add_data():
    select_sql = '''
    SELECT c.*
    FROM (
        SELECT b.date, a.mainland_confirm_add
        FROM mainland_data AS a
        JOIN (SELECT DATE_FORMAT(update_date, '%Y-%m-%d' ) AS date, MAX(update_date) AS max_time 
       	      FROM mainland_data 
       	      GROUP BY date ) AS b 
        ON b.max_time = a.update_date
        ORDER BY a.update_date DESC
        LIMIT 7
    ) AS c
    ORDER BY c.date  
    '''
    return query(select_sql)

# 获取最近7天本土每日新增无症状数据
def get_recent_mainland_daily_asymptomatic_add_data():
    select_sql = '''
    SELECT c.*
    FROM (
        SELECT b.date, a.mainland_asymptomatic_add
        FROM mainland_data AS a
        JOIN (SELECT DATE_FORMAT(update_date, '%Y-%m-%d' ) AS date, MAX(update_date) AS max_time 
       	      FROM mainland_data 
       	      GROUP BY date ) AS b 
        ON b.max_time = a.update_date
        ORDER BY a.update_date DESC
        LIMIT 7
    ) AS c
    ORDER BY c.date 
    '''
    return query(select_sql)

#获取累计确诊最多的5个省份/地区(不包含港澳台)
def get_total_confirm_top5_mainland_data():
    select_sql = '''
    SELECT province,SUM(confirm) as confirm
    FROM details_data
    WHERE province != "香港" 
          AND province != "澳门" 
          AND province != "台湾" 
          AND update_date = (SELECT update_date 
                            FROM details_data 
                            ORDER BY update_date DESC 
                            LIMIT 1)
    GROUP BY province
    ORDER BY confirm DESC
    LIMIT 5
    '''
    return query(select_sql)

#获取累计确诊最多的5个省份/地区(包含港澳台)
def get_total_confirm_top5_data():
    select_sql = """
    SELECT province ,SUM(confirm) AS `confirm_sum` 
    FROM details_data
    WHERE update_date = ( 
        SELECT update_date 
        FROM details_data 
        ORDER BY update_date DESC 
        LIMIT 1 )
    GROUP BY province 
    ORDER BY confirm_sum DESC 
    LIMIT 5
    """
    return query(select_sql)

#获取当天新增确诊最多的5个省份/地区（不包含港澳台）
def get_today_confirm_add_top5_mainland_data():
    select_sql = '''
        SELECT province,SUM(confirm_add) as confirm_add
            FROM details_data
            WHERE province != "香港" 
                AND province != "澳门" 
                AND province != "台湾" 
                AND update_date = (SELECT update_date 
                                    FROM details_data 
                                    ORDER BY update_date DESC 
                                    LIMIT 1  )
            GROUP BY province
            ORDER BY confirm_add DESC
            LIMIT 5
        '''
    return query(select_sql)

#获取当天新增确诊最多的5个省份/地区（包含港澳台）
def get_today_confirm_add_top5_data():
    select_sql = """
    SELECT province,SUM(confirm_add) as confirm_add 
    FROM details_data
    WHERE update_date=(
        SELECT update_date 
        FROM details_data 
        ORDER BY update_date DESC 
        LIMIT 1)
    GROUP BY province
    ORDER BY confirm_add DESC
    LIMIT 5
    """
    return query(select_sql)

#取省市详细表的最新更新时间，放到网页的某个地方，显示数据更新的时间
def get_data_update_date():
    select_sql='''
    SELECT update_date 
    FROM details_data 
    ORDER BY update_date DESC 
    LIMIT 1;
    '''
    return query(select_sql)[0][0]

#获取风险地区数据，获取的数据格式[[省A，市A，区A，社区A，风险等级A],[省B，市B，区B，社区B，风险等级B]。。。。]
def get_risk_area_date():
    select_sql=f'''
    SELECT province,city,county,community,grade
    FROM risk_area_data
    WHERE update_date = 
          (SELECT update_date 
          FROM risk_area_data
          ORDER BY update_date DESC
          LIMIT 1
          )
    '''
    data = query(select_sql)
    list = []
    for a in data:
        province = a[0]
        city = a[1]
        county = a[2]
        community = a[3]
        grade = a[4]
        list.append([grade,province,city,county,community])
    return list

#获取风险地区更新时间
def get_risk_area_update_date():
    select_sql=f'''
    SELECT update_date
    FROM risk_area_data
    ORDER BY update_date DESC
    LIMIT 1
    '''
    return query(select_sql)[0][0]

#获取高风险地区数量
def get_high_risk_area_number():
    select_sql= f'''
    SELECT COUNT(*)
    FROM risk_area_data 
    WHERE grade = "高风险"
    AND update_date = (SELECT update_date 
          FROM risk_area_data
          ORDER BY update_date DESC
          LIMIT 1);
    '''
    return query(select_sql)[0][0]

#获取低风险地区数量
def get_low_risk_area_number():
    select_sql= f'''
    SELECT COUNT(*)
    FROM risk_area_data 
    WHERE grade = "低风险"
    AND update_date = (SELECT update_date 
          FROM risk_area_data
          ORDER BY update_date DESC
          LIMIT 1);
    '''
    return query(select_sql)[0][0]

    
#获取一个省的词典，用于风险查询
# def get_province_list():
#     province_list= []
    # province_city_dict = {}
    # tmp_city_list = []
    # select_sql_1 = '''
    # SELECT DISTINCT province
    # FROM risk_area_data
    # WHERE update_date = 
    #       (SELECT update_date 
    #       FROM risk_area_data
    #       ORDER BY update_date DESC
    #       LIMIT 1
    #       )
    # '''  
    # for i in query(select_sql_1):
    #     province_list.append(i[0])
    # return province_list
    # for i in query(select_sql_1):
    #     province_city_dict[i[0]] = []
    # for j in province_city_dict.keys():
    #     tmp_city_list.clear()
    #     select_sql_2 = f'''
    #         SELECT DISTINCT city
    #         FROM risk_area_data
    #         WHERE province = "{j}"
    #         AND update_date = 
    #             (SELECT update_date 
    #             FROM risk_area_data
    #             ORDER BY update_date DESC
    #             LIMIT 1
    #             )
    #     ''' 
    #     for k in query(select_sql_2):
    #         province_city_dict[j].append(k[0])
    # return province_city_dict



