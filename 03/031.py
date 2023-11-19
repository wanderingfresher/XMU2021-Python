# 关联度分析

import pandas as pd
import csv
import re
import copy

class SearchTerm:
    def __init__(self,name,tag=0,s=''):
        self.name=name
        self.tag=tag
        self.root=s

id ={}
rel_dict=[]
reltmp=''
reltree={}
#是否可以字典读取
# colname=['id','name','关系']
file='01.csv'
with open(file, 'r' ,encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    i=0
    for row in reader:
        if i==0:
            i=1
            continue
        id.update({row[0]:SearchTerm(row[1])})

        reltmp=row[3]
        b = re.split('@|:|\n', reltmp)
        del b[-1]
        j=0

        rellist2={}
        for t in b:
            j=j+1
            if j%3==0:
                rellist2.update({b[j-1]:b[j-3]})
        reltree.update({row[0]: rellist2})
        i+=1



'''检查该节点子节点是否为空或者子节点均被检查过,
有一个为0,则该节点本轮不弹出,在其后继续将其子节点入栈saveQ
因为有一个为0,则意味着其还有未检查的子节点在workQ中
均为非0与非1,则其子节点均处理完,则可弹出'''
def judgeNode(ele):
    # print(ele)
    for x in reltree[ele].keys():
        # print(x,id[x].tag,end='  ')
        if id[x].root==ele or id[x].root=='':
            if id[x].tag == 0 or id[x].tag == 1:
                return 1
    return 0

df = pd.read_csv('01.csv')

idn = df['id'].values.tolist()
idm=set(idn)

'''dfs搜索记录一条关系链'''

start = input('请输入id:')
end = input('请输入id:')
id2=copy.deepcopy(id)
workQ = []
saveQ = [start]
id[start].tag=2


def dfs(elem,end,workQ,saveQ):
    i = 0
    while 1:
        ele = saveQ[-1]
        if judgeNode(ele) == 1:
            if i==0:
                i=9
                # print(i, saveQ)
            else:

                ele = workQ.pop(-1)
                saveQ.append(ele)
                id[ele].tag = 2
                # print(i, saveQ)
        else:

            a=saveQ.pop(-1)
            id[a].tag=3

            if saveQ==[]:
                break
            # print(i, saveQ)
            continue
        i += 1
        # print(i, saveQ)
        if ele == end:
            return 1

        for x in reltree[ele].keys():
            if id[x].root=='':
                id[x].root=ele
            if id[x].tag == 0:
                id[x].tag = 1
                workQ.append(x)

        # print(workQ, 'qqq')
        # print(saveQ, 'aaa')


dfs(start,end,workQ,saveQ)

# def search():

if saveQ==[]:
    print("未找到正序关系,开始查找反序关系")
    id = copy.deepcopy(id2)
    start, end = end, start
    workQ = []
    saveQ = [start]
    id[start].tag = 2
    dfs(start,end,workQ,saveQ)

def print_chain():
    i = 0
    for x in saveQ:
        if i == 0:
            print(x, id[x].name, end='')
            i = 1
            y = x
            continue
        y = saveQ[i - 1]
        print('', '的', reltree[y][x], '是', x, id[x].name, end='')
        if i % 5 == 0:
            print()
        i += 1

if saveQ==[]:
    print("正反序均未查到关系,该数据库中二者没有中介人物关系")
else:
    print('找到一条人物关系链,长度为%d'%(len(saveQ)))
    print('输出链条')
    print_chain()
