try:
    import requests
    from lxml import etree
except ImportError:
    pass
from urllib.request import urlretrieve
import os
import re
import time
from queue import Queue
import threading


class Producer(threading.Thread):
    def __init__(self,page_q,img_q,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.page_q = page_q
        self.img_q = img_q

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            self.i = re.search(r'\d+',url).group()
            self.parse_page(url,int(self.i))

    def parse_page(self,url, page):
        times = 1
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }
        res = requests.get(url, headers=headers)
        text = res.content.decode("utf-8")
        html = etree.HTML(text)
        imgs = html.xpath('//div[@class="page-content text-center"]//a/img[@class!="gif"]')
        if os.path.exists("../Pictures"):
            pass
        else:
            os.mkdir('../Pictures')
        for img in imgs:
            pagename = "../Pictures/page%d" % page
            if os.path.exists(pagename):
                pass
            else:
                os.mkdir(pagename)
            img_url = img.get("data-original")
            suff = os.path.splitext(img_url)[1]
            name = '%s/page%d-%d%s' % (pagename, page, times, suff)
            self.img_q.put((img_url,name))
            times += 1


class Consumer(threading.Thread):
    def __init__(self,page_q,img_q,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.page_q = page_q
        self.img_q = img_q

    def run(self):
        while True:
            img_url,name = self.img_q.get()
            urlretrieve(img_url,name)
            print('Loading.'+name)
            if (self.img_q.empty() and self.page_q.empty()):
                break

def main():
    print("注意：此程序将会在当前您的目录下创建一个新的Pictures目录来保存图片,如果您存在"
          "Pictures目录，将会在您的Pictures目录下下载表情包,如果不同意，\n请输入exit()来退出程"
          "序，否则请输入需要爬取的页数，页数小于3000（外部库依赖:requests,lxml），（仅限调试时：调试时使用前请确保"
          "已经下载好这两个\n库，或者在下面的输入框中输入”下载库“后自动下载（自动下载需要把Python加入环境变量中）,然后重新运行程序，使用exe版本的请忽略括号中的话，exe如果\n输入的话有大概率会"
          "报错，但是exe文件夹中内置了这两个库，请放心使用!）(暂不支持自定义下载文件夹，请期待更新)\n\t\t\t\t\t\t\t\t\t--开发者寄言")
    a = input("Please input the pages that you need(pages<3000) or exit() or ‘下载库’:")
    a = re.sub(r"[\'\"‘’“”]+","",a)
    if a =="下载库":
        os.system("pip install requests")
        os.system("pip install lxml")
        return
    else:
        try:
            a = int(a)
        except ValueError:
            print("退出程序")
            return
    if a < 3000:
        pass
    else:
        return
    page_q = Queue(a)
    img_q = Queue(1000)
    for i in range(1, a+1):
        url = "https://www.doutula.com/photo/list/?page=%d" % i
        page_q.put(url)
    for x in range(5):
        t = Producer(page_q,img_q)
        t.start()
    for i in range(5):
        t1 = Consumer(page_q,img_q)
        t1.start()


if __name__ == "__main__":

    main()
