import re
import csv
import copy
import urllib
import requests
from lxml import etree
from urllib import parse
from urllib import request
from bs4 import BeautifulSoup

import time
import random

# time功能
# time.sleep(random.random()*2)
n = 0

# 储存结构体
class Person:
    id = ''
    name = ''
    count = 0

    def __init__(self, s1='', s2='', n=0):
        self.id = s1
        self.name = s2
        self.count = n

# 全局变量设置
# 用列表行使队列操作
workQ = []  # 进行广度遍历的工作队列 储存id与姓名
saveQ = []  # 存储已经完成爬取的人物id与姓名与同名人物次序

# 网页 用urllib或requests爬取
def getHtml(url):
    # 延时
    time.sleep(random.random() * n)

    # 用request库 爬取网页
    # 重构请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

    req = requests.get(url)
    req.encoding = "utf-8"
    html = req.text
    return html

# 关系  通过request抓包
def getRelation(id, name, url):
    # 延时
    time.sleep(random.random() * n)
    # 爬取关系 b  抓包

    headers = {
        'User-Agent ': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/111.0.0.0 Safari/537.36 Edg',
        # 必须加cookie,虽然不知道咋加
        'Cookie': '',
        'Accep': '',
        "Referer": url
    }
    # 将API链接的查询实符串传给Params参数
    params = {
        'lemmaId': id,
        'lemmaTitle': name
    }

    # 暂时避免不了request爬取抓包
    res = requests.get('https://baike.baidu.com/starmap/api/gethumanrelationcard', headers=headers, params=params,
                       allow_redirects=False)
    # 返回结果力JSQN格式,调用json.()方法解析
    items = res.json()
    b = []
    # 拼接成如'好友:李白@1043\n好友:苏涣@10652\n' 标准形式
    for x in items['list']:
        s = x['relationName'] + ':' + x['lemmaTitle'] + '@' + str(x['lemmaId']) + '\n'
        b.append(s)
    b = "".join(b)

    return b

# 基本信息
def getBasic(html):
    # 解析基本信息 a
    soup = BeautifulSoup(html, features="html.parser")
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

    return a

# 介绍
def getIntro(html):
    # 解析介绍 c
    # 构造 _Element 对象
    html1 = etree.HTML(html)
    # 使用 xpath 匹配数据，得到匹配字符串列表
    sen_list = html1.xpath(
        '//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()')
    # 过滤数据，去掉空白
    sen_list_after_filter = [item.strip('\n') for item in sen_list]
    # 将字符串列表连成字符串并返回
    c = ''.join(sen_list_after_filter)
    c = re.sub(u"\\[.*?]", "", c)

    return c

# 经历
def getExperence(intro, html):
    # 解析生平 d

    # 构造 _Element 对象
    html1 = etree.HTML(html)
    sen_list = html1.xpath('//div[contains(@class,"para")]//text()')
    # 过滤数据，去掉空白
    sen_list_after_filter = [item.strip('\n') for item in sen_list]
    # 将字符串列表连成字符串并返回
    d = ''.join(sen_list_after_filter)
    d = re.sub(u"\\[.*?]", "", d)
    # 由于履历中有介绍重复一部分,将这一部分正则除去
    d = d.replace(intro, '', 1)

    return d

# 获得初始人物id,注意 整个程序中仅执行一次,仅根据初始人物数量决定
def spiderGetFirstId(content):
    url = 'https://baike.baidu.com/item/' + parse.quote(content)

    # 获取目标网址所有信息
    demo = getHtml(url)  # 定义所有信息的文本
    soup = BeautifulSoup(demo, 'html.parser')  # BeautifulSoup中的方法

    a = soup.find('link', rel="alternate", hreflang="x-default")
    a = a.get('href')
    a = a.split('/')[-1]  # 获得lemmaid
    # time.sleep(random.random() * n)
    # input("暂停")print(demo)
    return a

# 根据id,姓名构造网址
def urlConvert(id, name):
    url = 'https://baike.baidu.com/item/' + parse.quote(name) + '/' + id
    return url

# 对输入姓名进行归一化处理,以满足自定义数据结构
def intializeInputName(content):
    id = spiderGetFirstId(content)
    name = content
    return Person(id, name, 0)

# 执行四项信息爬取
def spiderBaidubaike(id, name):
    url = urlConvert(id, name)
    html = getHtml(url)
    relation = getRelation(id, name, url)
    basic = getBasic(html)
    intro = getIntro(html)
    experience = getExperence(intro, html)

    # print(relation)
    # print(basic)
    # print(intro)
    # print(experience)
    return relation, basic, intro, experience

# 写入
def csvWriteInfo(id, name, count, relation, basic, intro, experience):
    order = str(total).zfill(6)  # 序号
    row = [{
        'id': id,
        'name': name,
        '同名次序': count,
        '关系': relation,
        '基本信息': basic,
        '简介': intro,
        # '经历': experience

    }]
    # 按照列标题写入
    with open(filename, 'a+', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(row)

    # 将经历单独写入新文件txt,按次序对应命名

    with open('experience\\' + order + name + '@' + id + '.txt', 'w+', encoding='utf-8-sig', newline='') as f:
        f.write(experience)

# 中心人物的关系提取处理后装入工作队
def updateWorkQ(relation):
    # 以下处理将关系字符串分为关系名,名字,id三个一组的列表
    b = re.split('@|:|\n', relation)
    i = 0
    name = []
    id = []
    # 首位为1计数下标,模3为2即为名字,整除即为id, 分别加入相应列表
    for t in b:
        i = i + 1
        if i % 3 == 2:
            name.append(t)
        elif i % 3 == 0:
            id.append(t)
            n = i // 3 - 1
            # 每处理3个,取两个列表的同下标元素为一组,初始化个人信息,入工作队
            a = Person(id[n], name[n])
            workQ.append(a)

# 执行爬取,返回多条信息,写入,更新工作队
def spiderSearchWrite(ele):
    # 获得信息  ,basic,intro,experience     ,basic, intro, experience='','',''
    relation, basic, intro, experience = spiderBaidubaike(ele.id, ele.name)

    # 写入文件
    csvWriteInfo(ele.id, ele.name, ele.count, relation, basic, intro, experience)
    # 更新工作队,数目大于N个,不再入队,减少损耗,但如果要遍历所有人物,还是要放开跑
    if len(workQ) <= 2 * N:
        updateWorkQ(relation)
    else:
        print("总数达到,不再入队")

# 四条信息  关系 基本信息  简介  经历  ,'基本信息','简介','经历'

# csv header
fieldnames = ['id', 'name', '同名次序', '关系', '基本信息', '简介']
filename = 'result_data.csv'
# 写入列标题
with open(filename, 'w+', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

total = 0
N = 3000
flag1 = 0
flag2 = 0
k = 0
# 可能不断输入姓名
print("请输入人物姓名:", end='')
start_time = time.time()
while 1:
    content = input()  # '成龙'

    ele = intializeInputName(content)
    workQ.append(ele)

    while 1:
        # 跳出条件
        # 完成爬取数目,总程序结束
        if total == N:
            flag1 = 1
            break
        # 工作队空了,终止本层循环,跳出,并提示再次输入,并且尽可能与第一个人物关系远一些
        elif workQ == []:
            flag1 = 2
            print("目前条目数不足,请再次输入人物,尽可能与之前输入人物关系较远:", end='')
            break

        # 从工作队取出一个元素,查重,计数并储存
        ele = copy.deepcopy(workQ.pop(0))

        # 以下为对出队元素进行检查,满足要求则进行检索爬取
        # 确定该名为第几个该名人物(为1则无重名,其为第一个)
        count = 1
        flag2 = 0
        for a in saveQ:
            if a.name == ele.name:
                if a.id != ele.id:
                    count = count + 1
                else:  # 当前人信息已经在储存队中
                    flag2 = 1
        # 当前人在储存队中,且之前工作队为空,即输入的为工作队仅有的元素,原输入不符合要求,此时要求重新输入
        if flag1 == 2 and flag2 == 1:
            print("该条目已爬取,请另外输入,要求同上:", end='')
            break
        # 在工作队非空的情况下,条目重复,直接跳过该轮循环
        elif flag2 == 1:
            continue
        # 重新输入后,新条目非重复,则置flag1为0,避免影响不同分支
        elif flag1 == 2 and flag2 == 0:
            flag1 = 0
        # 若该条信息首次出现,更新重复数,存入储存队,总数加1
        ele.count = count
        saveQ.append(ele)
        total = total + 1
        # 输出当前处理对象,以及加上他的关系后工作队个数
        print(total, ':', ele.name, ele.id, '    ', end='')
        print("此时工作队元素个数(检测是否爆栈):", len(workQ))
        # 执行爬取,写入,
        try:
            spiderSearchWrite(ele)
        except:
            print("故障中止结束")
            flag1 = 1
            break

    if flag1 == 1:
        print("总爬取写入结束")
        break
    elif flag1 == 2:
        pass

print("爬取总数total:", total)
end_time = time.time()
print("耗时:", (end_time - start_time))
