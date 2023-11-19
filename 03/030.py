# 数据计算

import pandas as pd
import csv
import re
import copy

class SearchTerm:
    def __init__(self,name,tag=0,s=''):
        self.name=name
        self.tag=tag
        self.root=s

class ATerm:
    def __init__(self,t='',s='0',a=0,b=0,c=0):
        self.id=t
        self.root=s
        self.out_d=a
        self.d=b
        self.dif = b
        self.in_d=c

id ={}
alist={}
blist=[]
clist={}
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
        rellist1=[]
        rellist2={}
        for t in b:
            j=j+1
            if j%3==0:
                rellist2.update({b[j-1]:b[j-3]})
                rellist1.append(b[j-1])
        reltree.update({row[0]: rellist2})
        i+=1
        #print(row[0])
        #创建并记录出度
        alist.update({row[0]:ATerm(row[0],'', len(rellist1),len(rellist1))})
        blist.append(row[0])
        clist.update({row[0]:rellist1})


# 对id列表迭代,分析入度,记录根,记录出度与度差
i=0

for x in blist:
    if i==0:
        alist[x].root='0'
        i+=1

    for y in clist[x]:
        alist[y].in_d+=1
        alist[y].d+=1
        alist[y].dif-=1
        if alist[y].root=='':
            alist[y].root=x

def evaluation():

    origin_list =list(alist.values())    #初始数据列表
    #根据度数降序排序列表
    d_list=sorted(origin_list,key=lambda x:(x.d,x.dif,x.id),reverse=1)
    #根据出度降序排序列表
    out_list=sorted(origin_list,key=lambda x:(x.out_d,x.d,x.id),reverse=1)
    #根据入度降序排序列表
    in_list=sorted(origin_list,key=lambda x:(x.in_d,x.d,x.id),reverse=1)
    #切片
    N = 11915
    n =  int(N*0.1)# 总数的10%
    TP, TN, FP, FN = 0, 0, 0, 0

    d_list=d_list[0:n]
    out_list=out_list[0:n]
    in_list=in_list[0:n]

    for x in out_list:
        if x in d_list:
            TP+=1
        else:
            FP+=1
            FN+=1
    TN=N-n-FP
    recall=TP/n
    precision=TP/n
    acc=(TP+TN)/N
    print('TP:%d,TN:%d,FP:%d,FN:%d'%(TP,TN,FP,FN))
    print('以度数为标准降序排列,取前10%','即%d个为核心人物'%(n),sep=',')
    print('以出度为标准降序排序,取前%d个预测,分析数据如下:'%(n))
    print('召回率:%f\n准确率:%f'%(recall,acc))
