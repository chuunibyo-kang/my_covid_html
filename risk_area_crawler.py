import hashlib
import time
import requests
import json
import datetime

#这是风险地区爬虫
#至于为什么单独出来，是因为难度大了很多，要重写，单独出来比较好

#我们在中国政府网中，用浏览器分析ajax数据，可以看到一个interfacejson中包含大量的数据
#数据URL为http://bmfw.www.gov.cn/bjww/interface/interfaceJson



def get_risk_area_data():

    #设置时间戳
    timestamp = str(int(time.time()))

#wif签名
    x_wif_signature_str = timestamp + \
        'fTN2pfuisxTavbTuYVSsNJHetwq5bJvCQkjjtiLM2dCratiA'+timestamp
    x_wif_signature = hashlib.sha256(
        x_wif_signature_str.encode('utf-8')).hexdigest().upper()

#签名头
    signatureHeader_str = timestamp + \
        '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'+'123456789abcdefg'+timestamp
    signatureHeader = hashlib.sha256(
        signatureHeader_str.encode('utf-8')).hexdigest().upper()

    url = 'http://bmfw.www.gov.cn/bjww/interface/interfaceJson'

    #请求头的编写
    headers = {
        'Accept': "application/json, text/plain, */*",
        'Content-Type': "application/json;charset=utf-8",
        'x-wif-nonce': "QkjjtiLM2dCratiA",
        'x-wif-paasid': "smt-application",
        'x-wif-signature': x_wif_signature,
        'x-wif-timestamp': timestamp,
    }


    #定义一个字典，里面放置的内容是payload，没有这个payload无法访问网页，会返回500
    From_data_dir = {"key":"3C502C97ABDA40D0A60FBEE50FAAD1DA",
        "appId":"NcApplication",
        "paasHeader":"zdww",
        "timestampHeader": timestamp,
        "nonceHeader":"123456789abcdefg",
        "signatureHeader":signatureHeader}

    #另外，这个payload得是json，不然也会返回500
    From_data = json.dumps(From_data_dir )

    #发送请求
    response = requests.post(url=url, data=From_data, headers=headers)

    #如果访问成功，就返回请求数据，访问失败，就放出状态码
    if response.status_code != 200:
        return response.status_code
    else:
        #返回的数据是json，replace函数将“20yy-mm-dd xx时”里面的“xx时”换成“:00”
        #把时间更改后方便放入数据库
        return response.text.replace('\u65f6',':00')

# print(get_risk_area_data())

json_dir = json.loads(get_risk_area_data())

risk_area_update_date = datetime.datetime.fromisoformat(json_dir['data']['end_update_time'])


high_risk_dir = json_dir['data']['highlist']

low_risk_dir = json_dir['data']['lowlist']

