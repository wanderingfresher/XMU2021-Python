import re
import requests
import urllib
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from lxml import etree


def queryBaidubaike(content):
    #爬取基本信息
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
    # 重构请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

    req = requests.get(url)
    req.encoding = "utf-8"
    html = req.text
    soup = BeautifulSoup(req.text, features="html.parser")
    company_items = soup.find_all("div", class_="basic-info J-basic-info cmn-clearfix")
    a = []
    for i in company_items:
        x = i.text.strip()
        a.append(x)
    a = "".join(a)
    a = "".join(a.split('\xa0'))
    a = "\n".join(a.split('\n\n'))
    a = re.sub(u"\\[.*?]", "", a)
    a = "\n".join(a.split('\n\n'))
    a = "\n".join(a.split('\n\n'))

    fo = open(content + ".txt", "w", encoding='utf-8')
    fo.write('基本信息\n\n')
    fo.write(a)
    fo.close()


    #爬取关系
    url = 'https://baike.baidu.com/item/' + parse.quote(content)

    r = requests.get(url)  # 获取目标网址所有信息
    demo = r.text  # 定义所有信息的文本
    soup = BeautifulSoup(demo, 'html.parser')  # BeautifulSoup中的方法

    a = soup.find('link', rel="alternate", hreflang="x-default")
    a = a.get('href')
    a = a.split('/')[-1]

    headers = {
        'User-Agent ': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg',
        "Referer": url
    }

    # 损API链接的查询实符串传给Params参数
    params = {
        'lemmaId': a,
        'lemmaTitle': content
    }
    res = requests.get('https://baike.baidu.com/starmap/api/gethumanrelationcard', headers=headers, params=params)

    # 返回结果力JSQN格式,调用json.()方法解析
    items = res.json()
    a = []
    for x in items['list']:
        s = x['relationName'] + ':' + x['lemmaTitle'] + '\n'
        a.append(s)
    a = "".join(a)
    fo = open(content+".txt", "a+", encoding='utf-8')
    fo.write('\n\n人物关系\n\n')
    fo.write(a)
    fo.close()


    #爬取简介
    # 请求地址
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
    # 请求头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.99 Safari/537.36'
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    # 发送请求，获得响应
    response = urllib.request.urlopen(req)
    # 读取响应，获得文本
    text = response.read().decode('utf-8')
    # 构造 _Element 对象
    html = etree.HTML(text)
    # 使用 xpath 匹配数据，得到匹配字符串列表
    sen_list = html.xpath('//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()')

    # 过滤数据，去掉空白
    sen_list_after_filter = [item.strip('\n') for item in sen_list]
    # 将字符串列表连成字符串并返回

    b= ''.join(sen_list_after_filter)
    b=re.sub(u"\\[.*?]","",b)
    fo=open(content+".txt","a+", encoding='utf-8')
    fo.write('\n\n人物简介\n\n')
    fo.write(b)
    fo.close()



    #爬取履历
    sen_list = html.xpath('//div[contains(@class,"para")]//text()')

    # 过滤数据，去掉空白
    sen_list_after_filter = [item.strip('\n') for item in sen_list]
    # 将字符串列表连成字符串并返回

    a =''.join(sen_list_after_filter)
    a = re.sub(u"\\[.*?]", "", a)

    a=a.replace(b,'',1)
    fo = open(content + ".txt", "a+", encoding='utf-8')
    fo.write('\n\n人物履历:\n\n')
    fo.write(a)
    fo.close()


content=input('请输入:')
queryBaidubaike(content)
