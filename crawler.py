#爬虫核心
#提取网页json数据，获得最新的数据后更新数据库

import pymysql
import time
import traceback
import requests

# 模拟浏览器

from config import *

# 我们通过在Google chrome的浏览器检查中，找到了腾讯疫情数据接口
# 而modules后跟上的是对应数据的json名
# 这里跟上三个modules，能在一个页面力显示三份json数据
# 这三个json数据分别是中国疫情总情况、中国每日疫情总情况、各省具体疫情情况
def get_tencent_data():
    header = {'User-Agent':
                  r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'}
    target_url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,diseaseh5Shelf,provinceCompare'

#返回发出请求后返回的数据并将数据转成json，传入到response参数中
    resopnse = requests.get(target_url, headers=header).json()

#经过分析，返回的json是字典，而我们要的是data对应的value【数据核心】
    data = resopnse['data']

#新建一个空字典，用于存放历史数据
#预设结构 {日期：{确诊人数：xxxx},{确诊:xxxx},{治愈:xxxx},{死亡:xxxx}}
    history = {}
#循环遍历json里的ChinaDayList字典数据
    for i in data['chinaDayList']:
        #将chinaDayList里的y键value和date键value拼接起来
        #比如拼成2022.9.10
        string_data = i['y'] + '.' + i['date']
        #strptime方法将时间转成datatime对象，类型是元组
        #转换成一串很长的时间元组
        tuple_data = time.strptime(string_data, '%Y.%m.%d')
        #strftime方法将上面的那一组时间远祖转换成字符串时间的日期
        #比如转换成2022-09-10
        string_data = time.strftime('%Y-%m-%d', tuple_data)
        #给history字典对应的data键插入相应的数据
        history[string_data] = {'confirm': i['confirm'],
                       'heal': i['heal'], 'dead': i['dead']}

#循环遍历ChinaDayAddList这个json文件里的字典数据，这个json包含每天的疫情数据
#这里依旧要用到histroty字典
#对history字典里面的内容进行更新，变成如下：
# {日期：{确诊人数：xxxx},{确诊:xxxx},{治愈:xxxx},{死亡:xxxx},
#        {新增确诊:xxxx},{新增疑似:xxxx},{新增治愈:xxxx},{新增死亡:xxxx}}

    for i in data['chinaDayAddList']:
        #这里的时间转换和前面一个for循环内的一样
        #把YYYY.MM.DD转换成YYYY-MM-DD
        string_data = i['y'] + '.' + i['date']
        tuple_data = time.strptime(string_data, '%Y.%m.%d')
        string_data = time.strftime('%Y-%m-%d', tuple_data)
        #这一步判断在history字典里有没有对应的日期
        #如果没有对应日期，就不更新字典了，如果有对应日期，就更新该字典
        if string_data not in history.keys():
            continue
        #更新history词典，这里的键值名称和上一个chinaDayList的一样，但是对应的值不一样，要注意
        history[string_data].update({'confirm_add': i['confirm'],
                            'heal_add': i['heal'], 'dead_add': i['dead']})

    #获取具体的更新日期（精确到秒），作为的省市详细表的更新时间
    update_date = data['diseaseh5Shelf']['lastUpdateTime']

    #新创建一个details列表，用于存放具体的疫情数据
    details = []
    
    #根据对json数据的分析，省份数据在多个嵌套字典的值
    #省份数据在diseaseh5Shelf值里的areaTree字典值里的第1个里children字典值内
    province_data = data['diseaseh5Shelf']['areaTree'][0]['children']
    #遍历province_data的数据
    for province_infos in province_data:
        province_name = province_infos['name']#获取省份名
    #获取到省名称后，遍历地级市的信息
        for city_infos in province_infos['children']:
            #获取地级市名称
            city_name = city_infos['name']
            #获取城市累计确诊数量
            detail_confirm = city_infos['total']['confirm']
            #获取城市新增确诊数量
            detail_confirm_add = city_infos['today']['confirm']
            #获取城市累计治愈数量
            detail_heal = city_infos['total']['heal']
            #获取城市累计死亡数量
            detail_dead = city_infos['total']['dead']
    #最后将更新时间、省份名称、地级市名称、具体累计确诊人数、
    #     具体每日新增人数、具体的治愈人数、具体的死亡人数放入到一个列表中
    #再将生成的列表放到details列表中
            details.append([update_date, province_name, city_name, detail_confirm,
                            detail_confirm_add, detail_heal, detail_dead])
    
    
    #以下五项本土数据分别是更新时间、现有确诊、今日新增确诊、现有无症状、今日新增无症状
    mainland_data = data['diseaseh5Shelf']['chinaTotal']
    mainland_confirm_now = mainland_data['localConfirm']
    mainland_confirm_add = mainland_data['localConfirmAdd']
    asymptomatic_now = mainland_data['noInfectH5']
    asymptomatic_add = mainland_data['localWzzAdd']    
    #用一个嵌套列表把本土数据装起来
    mainland = [[update_date, mainland_confirm_now, 
    mainland_confirm_add, asymptomatic_now, 
    asymptomatic_add]]
    
    #这是获取腾讯数据函数里的最后一句话，
    #返回history词典、details列表和mainland列表这几个数据集，用于注入数据库中  
    return {'history':history, 'details':details,'mainland':mainland}

#连接接数据库
def db_connect():
    db_connect = pymysql.connect(
        host=HOST, 
        user=USER, 
        password=PASSWORD,
        database=DATABASE)
    return db_connect


#更新历史数据，这里指定传入data数据字典里的字典
#用try except捕获并处理异常，方便修改错误
def update_history_data(data:dict):
    try:
        #连接数据库
        db = db_connect()
        #输出时间，并表明开始更新历史数据
        print(f'{time.asctime()} 开始更新历史数据')
        #创建游标，用于执行SQL语句
        cursor = db.cursor()
        #这一句查询用于按日期查询数据表
        #用于后续for循环里的第二个if判断
        select_sql = 'SELECT confirm FROM history_data WHERE update_date=%s'
        #遍历data字典里的key和value
        for k, v in data.items():
            #data字典里的k是日期，v是一个字典，里面包含了多项数据
            #keys()函数用于返回字典的所有键
            #如果这些键的数量不足6，就跳过遍历，不执行后面的语句
            #【如果键数量不足6个，插入的数据对不上表头】
            if len(v.keys()) != 6:
                continue
            #这里执行一下前面定义好的select_sql语句，k值传入到sql语句的%s中
            #如果前面的select_sql执行成功了，以下这个if不执行
            #如果前面的select_sql没执行，就执行里面的insert_sql语句，避免重复写入。
            if not cursor.execute(select_sql, k):
                insert_sql = f'''
                            INSERT INTO history_data VALUES('{k}',{v['confirm']},{v['confirm_add']}, 
                            {v['heal']},{v['heal_add']},{v['dead']},{v['dead_add']})'''
                cursor.execute(insert_sql)
        #事务提交
        db.commit()
        print(f'{time.asctime()} 完成更新历史数据')
    except:
        #如果前面try里面的语句无法执行成功，就报错，方便排查
        traceback.print_exc()
    finally:
        #无论是否出错，这个都会执行
        #如果cursor仍然存在，就关闭
        if cursor:
            cursor.close()

#更新具体省份数据，这里指定传入data数据字典里的列表
def update_details_data(data:list):
    try:
        #连接数据库
        db = db_connect()
        cursor = db.cursor()
        # 子查询，选中update_time字段，按照id字段的降序排列顺序
        # 将子查询返回的时间与我们传入的时间比较，选出update_time里最新的时间
        # 经过测试，如果日期匹配，会返回1，如果日期不匹配，会返回0
        query_sql = '''
            SELECT %s > (
            SELECT update_date 
            FROM details_data
            ORDER BY update_date DESC
            LIMIT 1)
        '''
        #设定插入语句，用于后续更新
        insert_sql = f'''
        INSERT INTO 
        details_data (update_date,province,city,confirm,confirm_add,heal,dead) 
        VALUES(%s,%s,%s,%s,%s,%s,%s)'''
        #这个语句用于执行query_sql语句，用于后续的判断
        #data[0][0]取出的是第一个省数据的第一项日期元素，传入%s，用于与数据库最新的日期数据对比
        cursor.execute(query_sql, data[0][0]) 
        # cursor.fetchone用于返回执行结果
        # 如果query_sql执行返回的是0，则result结果为None
        # 如果query_sql执行返回的是1，则result结果为0
        result = cursor.fetchone()[0]
        #如果result结果不为0，即数据库没有最新数据，就会执行第一个if语句，更新最新数据
        #反之，则提示已是最新的数据
        if result != 0:
            print(f'{time.asctime()} 开始更新各省数据')
            for item in data:
                cursor.execute(insert_sql, item)
            print(f'{time.asctime()} 完成更新各省的数据')
        else:
            print(f'{time.asctime()} 已是最新的各省数据')
        #事务提交
        db.commit()
    except:
        #如果前面try里面的语句无法执行成功，就报错，方便排查
        traceback.print_exc()
    finally:
        #无论是否出错，这个都会执行
        #如果cursor仍然存在，就关闭
        if cursor:
            cursor.close()

# 这里更新本土数据，指定传入的数据是列表
def update_mainland_data(data:list):
    try:
        #连接数据库
        db = db_connect()
        cursor = db.cursor()
        # 子查询，选中update_time字段，按照id字段的降序排列顺序
        # 将子查询返回的时间与我们传入的时间比较，选出update_time里最新的时间
        # 经过测试，如果日期匹配，会返回1，如果日期不匹配，会返回0
        query_sql = '''
        SELECT %s > (
            SELECT update_date 
            FROM mainland_data
            ORDER BY update_date DESC
            LIMIT 1
        )
        '''
        #设定查询语句，用于后续更新
        insert_sql = f'''
        INSERT INTO 
        mainland_data (update_date,mainland_confirm_now,mainland_confirm_add,mainland_asymptomatic_now,mainland_asymptomatic_add) 
        VALUES(%s,%s,%s,%s,%s)'''
        #这个语句用于执行query_sql语句，用于后续的判断
        #data[0][0]取出的是第一个省数据的第一项日期元素，用于与数据库最新的数据对比
        cursor.execute(query_sql, data[0][0]) 
        # cursor.fetchone用于返回执行结果
        # 如果query_sql执行返回的是0，则result结果为None
        # 如果query_sql执行返回的是1，则result结果为0
        result = cursor.fetchone()[0]
        #如果result结果不为0，就会执行第一个if语句，更新最新数据
        #反之，则提示已是最新的数据
        if result != 0:
            print(f'{time.asctime()} 开始更新本土数据')
            for item in data:
                cursor.execute(insert_sql, item)
            print(f'{time.asctime()} 完成更新本土的数据')
        else:
            print(f'{time.asctime()} 已是最新的本土数据')
        #事务提交
        db.commit()
    except:
        #如果前面try里面的语句无法执行成功，就报错，方便排查
        traceback.print_exc()
    finally:
        #无论是否出错，这个都会执行
        #如果cursor仍然存在，就关闭
        if cursor:
            cursor.close()

#将抓取数据、更新数据的方法集中在crawler_run方法里，能做到调用一个方法就能抓取并更新数据
def crawler_run():
    db = db_connect()
    #获取网页json数据，传入data中
    tencent_data = get_tencent_data()
    #调用更新历史数据和具体数据方法
    update_history_data(tencent_data['history'])
    update_details_data(tencent_data['details'])
    update_mainland_data(tencent_data['mainland'])
    #关闭数据库
    db.close()

