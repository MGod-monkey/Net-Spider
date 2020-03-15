"""
第一PPT网爬取模块  官网：http://www.1ppt.com/
版本：1.0
"""
import requests as req
from lxml import etree
import os
import time
import zipfile

# 头部信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  "(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
}

main_url = "http://www.1ppt.com/"
path = os.path.join(os.path.expanduser("~"), 'Desktop') + "\\PPT"
path_list = [path]
cond1 = [1]
cond2 = [0]
if not os.path.exists(path):
    os.mkdir(path)


# 功能介绍
def introduct():
    print("""****************************************
    欢迎使用全自动PPT下载模块
    当前版本：1.0
    作者：@MGod吾
    受害者：http://www.1ppt.com/
    提示：
    1.为了方便，所有下载的PPT模块均为zip格式（其实就是不会解压，，，）
    2.该程序会在桌面自动创建一个PPT文件夹，下载的所有文件都在这里
    3.当前版本为初始版本，若使用过程遇到任何bug，欢迎反馈，邮箱：1781434602@qq.com
    
免责声明：当前模块提供的所有内容仅供学习、交流和分享用途，只供参考。
关于模块所爬取的内容均从网络上获得，仅供学习参考，请于24小时内删除。
使用本模块即表示您已经接受上述声明！需自行承担一切 风险与责任。
    """)
    time.sleep(2)
    print("\n\t模块正在运行，请稍等", end='')
    for t in range(0, 3):
        time.sleep(1)
        print("*", end='')
    print()
    print('>' * 30)


# 获取第一个选择
def get_first_choose(url, path, cond1, cond2):
    respose = req.get(url=url, headers=headers)
    respose.encoding = "gb2312"
    etr = etree.HTML(respose.text)
    # 第一分类
    first_type = etr.xpath("//div[@class='col_nav i_nav clearfix']/ul/li[@class='title']/text()")   # 第一分类的名称

    flag = 0    # 换行标记
    for num in range(0, len(first_type)):
        name = first_type[num]
        print(f"{str(num + 1)}.{name}\t", end='')
        flag += 1
        if flag == 3:
            flag = 0
            print()
    while True:
        try:
            print()
            choose = input("请选择你要下载的PPT模版类型(输入exit退出程序)：")
            if choose != "exit":
                choose = int(choose)
                cond2[0] = 1
                if choose > len(first_type):
                    print("没有该选项呢！")
                else:
                    path[0] += f"\\{first_type[choose]}"
                    if not os.path.exists(path[0]):
                        os.mkdir(path[0])
                    return choose
            else:
                cond1[0] = 0
                return None
        except Exception:
            print("请输入正确的选项！")


def get_second_choose(url, choose, path, cond2):
    respose = req.get(url=url, headers=headers)
    respose.encoding = "gb2312"
    etr = etree.HTML(respose.text)
    # 第二分类
    type_name = etr.xpath(f"//div[@class='col_nav i_nav clearfix']/ul[{str(choose)}]//a/text()")
    type_url = etr.xpath(f"//div[@class='col_nav i_nav clearfix']/ul[{str(choose)}]//a/@href")
    print(">" * 30)
    flag = 0
    for num in range(1, len(type_name) + 1):
        name = type_name[num-1]
        print(f"{num}.{name}\t", end='')
        flag += 1
        if flag == 3:
            flag = 0
            print()
    while True:
        try:
            print()
            second_choose = input("请选择你要下载的PPT模版(输入exit返回上一层)：")
            if second_choose != 'exit':
                second_choose = int(second_choose)
                if second_choose > len(type_name):
                    print("没有该选项呢！")
                    print()
                else:
                    path[0] += f"\\{type_name[choose]}"
                    if not os.path.exists(path[0]):
                        os.mkdir(path[0])
                    return "http://www.1ppt.com" + type_url[second_choose-1]
            else:
                cond2[0] = 0
                return None

        except Exception:
            print("请输入正确的选项！")


def download(url, path):
    PPT_num = 0
    print(">" * 30)
    start = time.perf_counter()
    respose = req.get(url=url, headers=headers)
    respose.encoding = "gb2312"
    etr =etree.HTML(respose.text)
    ppt_url = etr.xpath("//ul[@class='tplist']/li/a/@href")
    ppt_name = etr.xpath("//ul[@class='tplist']/li/a//@alt")
    for num in range(0, len(ppt_name)):
        name = ppt_name[num]
        print(f"{name}正在下载...")
        ppt_path = path[0] + f"\\{name}.zip"
        url = "http://www.1ppt.com" + ppt_url[num]
        respose = req.get(url=url, headers=headers)
        etr = etree.HTML(respose.text)
        download_url = etr.xpath("//ul[@class='downurllist']//a/@href")
        # 下载压缩包模块
        respose = req.get(url=download_url[0], headers=headers, stream=True)
        with open(ppt_path, "wb") as fp:
            for chunk in respose.iter_content(chunk_size=1024):
                if chunk:
                    fp.write(chunk)
        PPT_num += 1
        print(f"{name}已下载完成！")
    end = time.perf_counter()
    print(">" * 30)
    print("该模块下的PPT已全部下载完成！")
    print(f"路径：{path[0]}")
    print(f"共下载了{PPT_num}章PPT模块，耗时{end-start}s")
    print(">" * 30)
        # # 解压压缩包模块
        # r = zipfile.is_zipfile(ppt_path)
        # fz = zipfile.ZipFile(ppt_path, 'r')
        # for file in fz.namelist():
        #     fz.extract(file, path[0])


def main():
    introduct()
    while cond1[0]:
        first_choose = get_first_choose(main_url, path_list, cond1, cond2)
        while cond2[0]:
            second_url = get_second_choose(main_url, first_choose, path_list, cond2)
            if cond2[0]:
                download(second_url, path_list)
    print(">" * 30)
    print("感谢使用！！！")


if __name__ == '__main__':
    main()