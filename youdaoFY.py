import requests as req
import hashlib as hash
import random
import time
from lxml import etree

url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule/"
# 头部信息
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.116 Safari/537.36",
    "Cookie": r"P_INFO=wpqds666@163.com|1579875330|0|other|00&5|gux&1579800987"
              r"&mail163#gux&451100#10#0#0|&0|nmtp&urs&mail163&g98_client|"
              r"wpqds666@163.com; OUTFOX_SEARCH_USER_ID=1855731151@10.169.0.83;"
              r" JSESSIONID=aaax2Zh8Ygz-Z-pHZo8bx; OUTFOX_SEARCH_USER_ID_NCOO=113884837.0691015;"
              r" ___rl__test__cookies=1582632370604",
    "Referer": "http://fanyi.youdao.com/",
}


# 获取MD5的函数
def get_md5(string):
    string = string.encode('utf8')
    md5 = hash.md5(string).hexdigest()  # 返回摘要 32位字符串
    return md5


# 获取简单翻译解析内容
def easy(text):
    list = text.split('"')
    try:
        translate_word = list[5]  # 翻译结果
        find_word = list[9]  # 要翻译的单词
        print(f""">>>>>>>>>>>>>>>>>>>>>>>>>>>有道翻译（版本：2.1）>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                              翻译：{find_word}
                              结果：{translate_word}
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        （简单）翻译结果已显示，按回车键返回上一层。
    """)
    except IndexError:
        print("抱歉！找不到该单词！小道正在努力收集！")

# 翻译字符串为中文还是英文的函数,如果是中文返回True
def check_contain_chinese(string):
    for _char in string:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


# 获取详细页面的内容(分中英文)
def difficult(string):
    detail_utl = "http://dict.youdao.com/search?"
    get_data = {
        "q": string,
        "keyfrom": "new-fanyi.smartResult",
    }
    r = req.get(url=detail_utl, headers=header, params=get_data)
    terr = etree.HTML(r.text)
     # 翻译中文的情况下
    if check_contain_chinese(string):
        # //ul//span[@class="contentTitle"]/a/text() 详细页面的直译单词
        direct_trans = terr.xpath('//ul//span[@class="contentTitle"]/a/text()')
        print(direct_trans[0])
        # //div[@id='webPhrase']/p//text() 网络翻译短语
        # sort_list = [] # 存放短语的列表
        # word_trans = terr.xpath("//div[@id='webPhrase']/p//text()")
        # word_trans = [x.strip() for x in word_trans if x.strip() != '']
        # # 对短语进行处理
        # for i in word_trans:
        #     i = i.replace('\n', '').replace(' ', '')
        #     sort_list.append(i)
        # ':'.join(sort_list)
        # print(sort_list)
        # 英汉大字典解释
        # //ul[@class='ol wordGroup']/li[@class='wordGroup']/span
        # //ul[@class='ol wordGroup']/li
        # yh = terr.xpath("//ul[@class='ol wordGroup']/li")
        # english_trans = terr.xpath("//ul[@class='ol']/li//text()")
        # english_trans = [x.strip() for x in english_trans if x.strip() != '']
        # x = ''.join(english_trans)
        # for j in x:
        #     if check_contain_chinese(j):
        #         continue
        #     else:
        #         print()

        # print(yh)


# 　给一个要翻译的字符串，返回翻译结果
def FY(string=None, mode=None):
    # 反写js代码，获取sign，ts，bv，salt
    ts = str(int(time.time() * 1000))  # ts是个时间戳
    salt = ts + str(random.randint(0, 9))  # salt是ts+0到9随机数
    sign = get_md5("fanyideskweb" + string + salt + "Nw(nmmbP%A-r6U3EUn]Aj")
    version = "5.0 (Windows NT 10.0; Win64; x64) " \
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
    bv = get_md5(version)
    # POST表单
    datas = {
        "i": string,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "ts": ts,
        "bv": bv,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION",
    }
    r = req.post(url=url, headers=header, data=datas)
    if mode == '简单':
        easy(r.text)
    else:
        difficult(string)


def main():
    cond = True
    while cond:
        mode = input("请输入想要的翻译内容（简单 or 详细）：")
        if mode == '详细':
            print("抱歉！详细功能还在开发中，请您先使用简单的翻译功能吧！")
            cond2 = False
        elif mode == '简单':
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            cond2 = True
        else:
            print("请您输入正确的指令！！")
            cond2 = False
        while cond2:
            string = input("请输入你要翻译的单词(自动检测)：")
            if string != '':
                FY(string, mode)
            else:
                cond2 = False


if __name__ == '__main__':
    main()
