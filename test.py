import requests

user_ip = "112.94.96.14"
url = f"https://ip.taobao.com/outGetIpInfo?ip={user_ip}&accessKey=alibaba-inc"
response = requests.get(url)
location_dict = {}
location_dict = response.json()
user_location = ""
if location_dict['data']['country'] == "中国":
    user_location = location_dict['data']['region']+location_dict['data']['city']
else:
    user_location = location_dict['data']['country']

print(user_location)