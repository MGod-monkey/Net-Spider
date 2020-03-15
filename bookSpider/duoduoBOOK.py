""""
多多小说网免费书籍爬取模块（官网：https://xs.sogou.com）
当前版本1.0
作者：@MGod吾
当前功能：多多小说网的免费小说第一页资源全爬，且能按文件分类好
当前问题：下载速度过慢，字数统计无法进行，下载的章节观感差，下载的页数仅限于个分类页面下的第一页
尝试增加模块：
1，断点续传
2，字数统计  （已实现）
    问题1：嵌套函数里的变量不能被调用
    解决1：通过在嵌套函数里调用其他函数，传参并返回
    发现：传入的参数分传值和传址，传值（int，str，元组）传址（dict，list）
    传值不会改变参数的数值，传址会
3，内容排序  (已实现)
4，免费资源全爬
5，尝试解决下载速度过慢

20/3/4  更新
版本1.1
更新内容：
1，加入规范写入文本模块
2，解决字数统计不能使用的问题
3，在每本书籍下载模块加入计时功能
"""
import requests as req
from lxml import etree
import os
import time
import re

# 用于统计的信息
all_time = [0]  # 下载计时
book_num = [0]  # 书籍数量
chapter_num = [0]  # 下载的总章节数
word_num = [0]  # 下载的总字数

# 头部信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  "(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
}
# 创建男女生分类的文件夹目录
man_dir = "man_type"
wom_dir = "wom_type"
if not os.path.exists(man_dir):
    os.mkdir(man_dir)
if not os.path.exists(wom_dir):
    os.mkdir(wom_dir)


# 获取分类页面不同类型小说的url
def get_main_url():
    main_url = "https://xs.sogou.com/0_0_1_0_heat/"
    respose = req.get(url=main_url, headers=headers)
    etr = etree.HTML(respose.text)
    # 解析网页，获取男女生分类的名称及对应的url
    man_type = etr.xpath("//ul[@pbflag='男生分类']//text()")
    man_type_name = [x.strip() for x in man_type if x.strip() != '']
    wom_type = etr.xpath("//ul[@pbflag='女生生分类']//text()")
    wom_type_name = [x.strip() for x in wom_type if x.strip() != '']
    man_type_url = etr.xpath("//ul[@pbflag='男生分类']//@href")
    wom_type_url = etr.xpath("//ul[@pbflag='男生分类']//@href")
    # 用于存放完整的url列表
    man_list = []
    wom_list = []
    for url in man_type_url:
        url = 'https://xs.sogou.com' + url
        man_list.append(url)
    for url in wom_type_url:
        url = 'https://xs.sogou.com' + url
        wom_list.append(url)
    # print(man_list)
    # 创建不同类型名称的目录
    for name in man_type_name:
        path = man_dir + "/" + name
        if not os.path.exists(path):
            os.mkdir(path)
    for name in wom_type_name:
        path = wom_dir + "/" + name
        if not os.path.exists(path):
            os.mkdir(path)
    # 创建类型字典并返回
    type_dict = {
        "man_type_name": man_type_name,
        "wom_type_name": wom_type_name,
        "man_type_url": man_list,
        "wom_type_url": wom_list,
    }
    return type_dict


# 获取字数的模块，解决嵌套函数内变量无法被调用的问题
def get_word_num(num):
    word_num = re.findall(r'\d+', num)
    return int(word_num[0])


# 传入文本，规范文本格式并写入文件中
def guifan_text(text, text_path):
    """

    :param text: 文本[]
    :param text_path: 文本路径
    :return: None
    """
    with open(text_path, 'a', encoding='utf8') as fp:
        fp.writelines(text[1:5])
    # final_text = text[1:5]
    for t in text[7:]:
        if t[0] != '\r\t':
            t = '\t' + t
        text_list = list(t)
        l = len(text_list)
        if l > 45:
            for i in range(1, l // 45 + 1):
                if text_list[40 * i] == '，' or "”" or "。":
                    text_list.insert(45 * i + 1, '\n')
                else:
                    text_list.insert(45 * i, '\n')
        text_list.append("\r\n")
        # final_text += text_list
        with open(text_path, 'a', encoding='utf8') as fp:
            fp.writelines(text_list)
    fp.close()


# 传入小说信息字典，开始下载小说
def download_book(book_name, book_url, type_name, type, chapter_num, word_num):
    """
    :param book_name: 小说名[]
    :param book_url: 小说目录url[]
    :param type_name: 分类类型名称[]
    :param type: 男女类型标识
    :param chapter_num: 章节数量统计
    :param word_num: 字数统计
    :return: None
    """
    # print(len(book_name))
    for num in range(0, len(book_name)):
        try:
            start = time.perf_counter()
            print("*" * 25)
            print(f"《{book_name[num]}》正在下载...")
            # 创建书籍名文件
            book_path = type + '/' + type_name + '/'
            respose = req.get(url=book_url[num], headers=headers)
            etr = etree.HTML(respose.text)
            url_list = etr.xpath("//a[@class='text-ellips']/@href")
            text_url = []
            for url in url_list:
                url = "https://xs.sogou.com" + url
                text_url.append(url)
            # print(text_url)
            # 下载章节模块
            flag1 = 1
            for url in text_url:
                # 在第一章收集信息
                if flag1:
                    respose = req.get(url=url, headers=headers)
                    etr = etree.HTML(respose.text)
                    book_info = etr.xpath("//div[@class='paper-box paper-cover']/p/text()")
                    for info in book_info:
                        print(info)
                    book_path = book_path + book_name[num] + f"-{book_info[0]}.txt"
                    word_num[0] += get_word_num(book_info[2])
                    # print(word_num)
                    text = etr.xpath("//div[@class='paper-box paper-article']//text()")
                    guifan_text(text, book_path)
                    # for t in text:
                    #     t = '\t' + t
                    #     l = len(t)
                    #     n = l / 40
                    #     if len(t) >
                    #     if t[-1] == '"' or "。":
                    #         t += '\n'
                    #         with open(book_path, 'a', encoding="utf8") as fp:
                    #             fp.write(t)
                        # else:
                        #     print(f"《{book_name[num]}》已存在！")
                        #     print("*" * 25)
                        #     flag1 = 0
                        #     flag2 = 1
                        #     chapter_num[0] -= 1
                        #     break
                    chapter_num[0] += 1
                    flag1 = 0
                else:
                    respose = req.get(url=url, headers=headers)
                    etr = etree.HTML(respose.text)
                    text = etr.xpath("//div[@class='paper-box paper-article']//text()")
                    guifan_text(text, book_path)
                    chapter_num[0] += 1
            end = time.perf_counter()
            print(f"《{book_name[num]}》已下载完成！耗时{end - start}s")
            print('*' * 25)
        except Exception:
            print("下载错误！已自动跳过！")


# 传入分类信息字典，获取相应书籍信息，并返回书籍名，书籍目录url的字典
def get_chapter_url(type_dict, book_num, chapter_num, word_num):
    """

    :param type_dict: 分类类型字典["man_type_name": man_type_name,
                                    "wom_type_name": wom_type_name,
                                    "man_type_url": man_list,
                                    "wom_type_url": wom_list,]
    :param book_num: 书籍数量统计
    :param chapter_num: 章节数量统计
    :param word_num: 字数统计
    :return: None
    """
    for n in range(0, len(type_dict["man_type_name"])):
        name = type_dict["man_type_name"][n]
        print(">" * 50)
        print(f"男-{name}类型小说正在下载>>>>>>")
        url = type_dict["man_type_url"][n]
        respose = req.get(url=url, headers=headers)
        etr = etree.HTML(respose.text)
        # 解析分类列表下的书籍信息
        book_name = etr.xpath("//h3//text()")
        book_num[0] = book_num[0] + len(book_name)
        book_url = []   # 设置一个用于存储书籍目录url的列表
        for url in etr.xpath("//div[@class='btns']/a[2]/@href"):
            url = "https://xs.sogou.com" + url
            book_url.append(url)
        download_book(book_name, book_url, name, 'man_type', chapter_num, word_num)
        # time.sleep(1)  # 缓冲1s
        # 女生小说下载模块
    for n in range(0, len(type_dict["wom_type_name"])):
        name = type_dict["wom_type_name"][n]
        print(">" * 50)
        print(f"女-{name}类型小说正在下载>>>>>>")
        url = type_dict["wom_type_url"][n]
        respose = req.get(url=url, headers=headers)
        etr = etree.HTML(respose.text)
        # 解析分类列表下的书籍信息
        book_name = etr.xpath("//h3//text()")
        book_num[0] = book_num[0] + len(book_name)
        book_url = []
        for url in etr.xpath("//div[@class='btns']/a[2]/@href"):
            url = "https://xs.sogou.com" + url
            book_url.append(url)
        download_book(book_name, book_url, name, 'wom_type', chapter_num, word_num)
        time.sleep(1)  # 缓冲1s


def main():
    start_time = time.perf_counter()
    # type_dict包含类型名称和url
    type_dict = get_main_url()
    get_chapter_url(type_dict, book_num, chapter_num, word_num)
    end_time = time.perf_counter()
    all_time = end_time - start_time
    print("多多小说网免费书籍已全部下载完成！")
    print(f"共下载{book_num[0]}本小说，累计{chapter_num[0]}个章节，耗时{all_time[0]}s")


if __name__ == '__main__':
    main()
