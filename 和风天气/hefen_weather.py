from requests import get
from time import sleep
import json
from lxml.html import etree
from socket import getfqdn, gethostbyname, gethostname

# # 获取本机电脑名
# myname = getfqdn(gethostname())
# # 获取本机ip
# myaddr = gethostbyname(myname)
# print(myaddr)
url = 'https://free-api.heweather.net/s6/weather/'
key = "369b82e6cfc44023b051d3b6f49e9624"    #和风天气查询的key

# 关键词字典
type_url = {
    '1': 'https://free-api.heweather.net/s6/weather/now',
    '2': 'https://free-api.heweather.net/s6/weather/forecast',
    '3': 'https://free-api.heweather.net/s6/weather/hourly',
    '4': 'https://free-api.heweather.net/s6/weather/lifestyle'
}
# 生活指数字典
life_key = {
    'comf': '舒适度指数',
    'cw': '洗车指数',
    'drsg': '穿衣指数',
    'flu': '感冒指数',
    'sport': '运动指数',
    'trav': '旅游指数',
    'uv': '紫外线指数',
    'air': '空气污染扩散条件指数',
    'ac': '空调开启指数',
    'ag': '过敏指数',
    'gl': '太阳镜指数',
    'mu': '化妆指数',
    'airc': '晾晒指数',
    'ptfc': '交通指数',
    'fsh': '钓鱼指数',
    'spi': '防晒指数'
}
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
data = {
    'location': '北京',
    'key': key
}


# 获取公网ip
def get_ip():
    url = "https://www.baidu.com/s?tn=88093251_47_hao_pg&ie=utf-8&wd=ip"
    response = get(url=url, headers=headers)
    etr = etree.HTML(response.text)
    ip_str = etr.xpath('//div[@class="c-span21 c-span-last op-ip-detail"]//text()')
    return ip_str[2] + ip_str[3].split("\n")[0]


class weather(object):
    pass


class Now_Weather(weather):
    def getweather(self, url):
        reposen = get(url=url, headers=headers, params=data)
        weather = json.loads(reposen.text)
        if weather['HeWeather6'][0]['status'] == 'ok':
            print(f"""********************************************\n
            成功查询到以下内容：
            城市ID：{weather['HeWeather6'][0]['basic']['cid']}
            所属城市：{weather['HeWeather6'][0]['basic']['location']},{weather['HeWeather6'][0]['basic']['parent_city']},{weather['HeWeather6'][0]['basic']['admin_area']},{weather['HeWeather6'][0]['basic']['cnty']}
            经纬度：{weather['HeWeather6'][0]['basic']['lon']},{weather['HeWeather6'][0]['basic']['lat']}
            城市所在时区：{weather['HeWeather6'][0]['basic']['tz']}

            当前天气：
            温度（摄氏度）：{weather['HeWeather6'][0]['now']['tmp']}
            体感温度（摄氏度）：{weather['HeWeather6'][0]['now']['fl']}
            天气状况：{weather['HeWeather6'][0]['now']['cond_txt']}
            风向：{weather['HeWeather6'][0]['now']['wind_dir']}
            风力：{weather['HeWeather6'][0]['now']['wind_sc']}
            风速(公里/小时)：{weather['HeWeather6'][0]['now']['wind_spd']}
            相对湿度（百分比）：{weather['HeWeather6'][0]['now']['hum']}
            降水量：{weather['HeWeather6'][0]['now']['pcpn']}
            大气压强（帕）：{weather['HeWeather6'][0]['now']['pres']}
            能见度（公里）：{weather['HeWeather6'][0]['now']['vis']}
            云量：{weather['HeWeather6'][0]['now']['cloud']}

            更新时间：
            本地时间：{weather['HeWeather6'][0]['update']['loc']}
            UTC时间：{weather['HeWeather6'][0]['update']['utc']}""")
            sleep(3)  # 强制停止3s
        else:
            print(f"》》》》发生了些不可描述的错误(error code：{weather['HeWeather6'][0]['status']})》》》》")


class Recent_Weather(weather):
    def getweather(self, url):
        reposen = get(url=url, headers=headers, params=data)
        print(data['location'])
        weather = json.loads(reposen.text)
        if weather['HeWeather6'][0]['status'] == 'ok':
            weather = json.loads(reposen.text)
            print(f"""********************************************\n
            成功查询到以下内容：
            城市ID：{weather['HeWeather6'][0]['basic']['cid']}
            所属城市：{weather['HeWeather6'][0]['basic']['location']},{weather['HeWeather6'][0]['basic']['parent_city']},{weather['HeWeather6'][0]['basic']['admin_area']},{weather['HeWeather6'][0]['basic']['cnty']}
            经纬度：{weather['HeWeather6'][0]['basic']['lon']},{weather['HeWeather6'][0]['basic']['lat']}
            城市所在时区：{weather['HeWeather6'][0]['basic']['tz']}

            3-10天天气预报：""", end='')
        n = 0
        for i in weather['HeWeather6'][0]['daily_forecast']:
            n += 1
            print(f"""
            第{n}天：

            预报日期：{i['date']}
            日出-日落时间：{i['sr']}-{i['ss']}
            月升-月落时间：{i['mr']}-{i['ms']}
            最高（低）温（摄氏度）：{i['tmp_max']}({i['tmp_min']})
            白天（晚上）天气状况：{i['cond_code_d']}({i['cond_code_n']})
            风向：{i['wind_dir']}
            风力：{i['wind_sc']}
            风速（公里/小时）：{i['wind_spd']}
            相对湿度（百分比）：{i['hum']}
            降水量：{i['pcpn']}
            大气压强（帕）：{i['pres']}
            能见度（公里）：{i['vis']}
        """, end='')
            print(f"""
            更新时间：
            本地时间：{weather['HeWeather6'][0]['update']['loc']}
            UTC时间：{weather['HeWeather6'][0]['update']['utc']}
            """)
            sleep(3)
        else:
            print(f"》》》》发生了些不可描述的错误(error code：{weather['HeWeather6'][0]['status']})》》》》")


class Lifeindex_Weather(weather):
    def getweather(self, url):
        reposen = get(url=url, headers=headers, params=data)
        print(data['location'])
        weather = json.loads(reposen.text)
        if weather['HeWeather6'][0]['status'] == 'ok':
            weather = json.loads(reposen.text)
            print(f"""********************************************\n
            成功查询到以下内容：
            城市ID：{weather['HeWeather6'][0]['basic']['cid']}
            所属城市：{weather['HeWeather6'][0]['basic']['location']},{weather['HeWeather6'][0]['basic']['parent_city']},{weather['HeWeather6'][0]['basic']['admin_area']},{weather['HeWeather6'][0]['basic']['cnty']}
            经纬度：{weather['HeWeather6'][0]['basic']['lon']},{weather['HeWeather6'][0]['basic']['lat']}
            城市所在时区：{weather['HeWeather6'][0]['basic']['tz']}""")
            for i in weather['HeWeather6'][0]['lifestyle']:
                print(f"""
            {life_key[i['type']]}: {i['brf']}
            温馨提醒：{i['txt']}
""", end='')
            print("""
            更新时间：
            本地时间：{weather['HeWeather6'][0]['update']['loc']}
            UTC时间：{weather['HeWeather6'][0]['update']['utc']}
""")
            sleep(3)
        else:
            print(f"》》》》发生了些不可描述的错误(error code：{weather['HeWeather6'][0]['status']})》》》》")


# 创建get_weather类
class Get_Weather(object):
    def search_weather(self, url):
        # 传入data,headers,url获取天气信息
        print(url)
        self.print_cd2()
        command = input("\n>>>请输入你要查询城市的方式：")
        try:
            if command != "5":
                city_id = input(">>>请输入你要查询的城市（默认北京）：")
                if city_id != '':
                    data["location"] = city_id
            else:
                data["location"] = 'auto_ip'
        except Exception as error:
            print("》》》》发生了些不可描述的错误》》》》/n" + error)
        self.weather.getweather(url)

    def print_cd(self, ip):
        print(f"""********************************************\n
        《和风天气》自助查询系统
            1: 实况天气
            2：3-10天预报
            3：逐小时预报
            4：生活指数
            5：帮助
    
{ip}
********************************************\n""")

    def print_help(self):
        print("""********************************************\n
帮助：
实况天气：
    实况天气即为当前时间点的天气状况以及温湿风压等气象指数，具体包含的数据：
体感温度、实测温度、天气状况、风力、风速、风向、相对湿度、大气压强、降水量、能见度等。
3-10天天气预报：
    3-10天天气预报数据，天气预报包含的数据：日出日落、月升月落、最高最低温度、
天气白天和夜间状况、风力、风速、风向、相对湿度、大气压强、降水量、降水概率、露点温度、紫外线强度、能见度等数据
逐小时预报：
    未来24-168个小时，逐小时的天气预报数据数据，具体包含的数据：温度、天气状况、风力、风速、风向、相对湿度、大气压强、降水概率等。
生活指数：
    生活指数和生活指数预报包括：穿衣、洗车、感冒、紫外线、运动、舒适度、旅游、空气污染扩散条件。
                """)

    def print_cd2(self):
        print("""********************************************\n
        1: 城市ID（自行查询城市列表）
        2：经纬格式（格式：经度,纬度）
        3：城市名称（格式：城市，省，国家（国家和省可略））
        4：IP（所要查询城市的IP）
        5: 动态IP（自动获取用户IP，准确性以用户所用的公网IP为准）
            
        """ + get_ip())


def main():
    get_weather = Get_Weather()

    while True:
        get_weather.print_cd(get_ip())
        command = input(">>>请输入你要查询的天气状况(exit退出)：")
        if command == "1":
            now_weather = Now_Weather()
            get_weather.weather = now_weather
            get_weather.search_weather(type_url[command])
        elif command == "2":
            recent_weather = Recent_Weather()
            get_weather.weather = recent_weather
            get_weather.search_weather(type_url[command])
        elif command == "3":
            print("此服务是VIP服务，作者贫穷，付不起高昂的vip费用，若有需要，可以联系作者（带上你的vip费用<-_<-）")
        elif command == "4":
            lifeindex = Lifeindex_Weather()
            get_weather.weather = lifeindex
            get_weather.search_weather(type_url[command])
        elif command == "5":
            get_weather.print_help()
        elif command == "exit":
            exit(1)
        elif command == "exit()" or command == "exit（）":
            print("\n无法识别的指令，如果您要退出请输入exit退出")
            sleep(2)
        else:
            print(">>>请输入正确的指令！！！")
            continue


if __name__ == '__main__':
    main()
