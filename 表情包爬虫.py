import requests
from lxml import etree
from urllib.request import urlretrieve
import os
def parse_page(url,page):
    times = 1
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    res = requests.get(url,headers=headers)
    text = res.content.decode("utf-8")
    html = etree.HTML(text)
    imgs = html.xpath('//div[@class="page-content text-center"]//a/img[@class!="gif"]')
    if os.path.exists("../Pictures"):
        pass
    else:
        os.mkdir('../Pictures')
    for img in imgs:
        pagename = "../Pictures/page%d"%page
        if os.path.exists(pagename):
            pass
        else:
            os.mkdir(pagename)
        img_url = img.get("data-original")
        suff = os.path.splitext(img_url)[1]
        name = '%s/page%d-%d%s'%(pagename,page,times,suff)
        print('Loading.'+name)
        urlretrieve(img_url,name)
        times += 1


def main():
    print("注意：此程序将会在当前您的目录下创建一个新的Pictures目录来保存图片,如果您存在Pictures目录，将会在您的Pictures下下载表情包,如果不同意，请输入exit()来退出程序，否则请输入需要爬取的页数，页数小于3000")
    a = input("Please input the pages that you need(pages<3000) or exit():")
    try:
        a = int(a)
    except:
        print("退出程序")
        return
    if a < 3000:
        pass
    else:
        return
    for i in range(1,a+1):
        url = "https://www.doutula.com/photo/list/?page=%d"%i
        parse_page(url,i)

if __name__ == '__main__':
    main()
