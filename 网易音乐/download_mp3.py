"""
该模块有下载mp3，歌词的功能
"""
import requests as req
from os import path, mkdir
from urllib import error
from time import perf_counter

url = "https://www.769sc.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  "(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


# 获取歌曲信息
def get_message(url):
    input_name = input("请输入你要下载的歌曲名：")
    datas = {
        "input": input_name,
        "filter": "name",
        "type": "netease",
        "page": "1",
    }
    try:
        response = req.post(url=url, headers=headers, data=datas)
        if response.json != "":
            return response.json()["data"]
    except error.HTTPError:
        print("网络错误！")


# 下载歌曲
def download_sing(message):
    n = 0
    for list in message:
        n += 1
        print(f'{n}.{list["title"]}-{list["author"]}')
    while True:
        try:
            number = int(input("请输入你要下载的歌曲：")) - 1
            file_name = message[number]["title"] + message[number]["author"]
            print(f"{file_name}正在下载...")
            if not path.exists(file_name):
                mkdir(file_name)
            sing_path = file_name + "\\" + file_name + ".mp3"
            lrc_path = file_name + "\\" + file_name + ".lcy"
            lrc_text_path = file_name + "\\" + file_name + ".txt"
            response = req.get(url=message[number]["url"])
            start = perf_counter()
            with open(sing_path, "ab") as fp:
                fp.write(response.content)
            with open(lrc_path, "w") as fp:
                fp.write(message[number]["lrc"])
            with open(lrc_text_path, "w", encoding="utf-8") as fp:
                fp.write(message[number]["lrc"])
            end = perf_counter()
            print(f"下载完成！耗时{end - start}s")
            print(">" * 50)
            return None
        except error.HTTPError:
            print("下载错误！")
        except Exception:
            print("请输入正确的指令！")


def main():
    while True:
        message = get_message(url)
        download_sing(message)
if __name__ == '__main__':
    main()