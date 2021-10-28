'''
Author: Jin
Date: 2021-10-27 10:23:02
LastEditors: Jin
LastEditTime: 2021-10-28 09:02:27
Description: transfer 2-d table into JSON format
'''
import json
import pandas as pd

file = r'.\\src\\P102060300025(1).xlsx'
t = pd.read_excel(file,skiprows=5)
t = t.iloc[:-6,1:]
t['id']=range(len(t))
cols=t.columns.tolist()
cols=cols[-1:]+cols[:-1]
t=t[cols]
t2j=t.to_json(orient="records",force_ascii=False)
j=json.loads(t2j)

'''
description: 
param {*} x
return {*} 返回x以上，与x的级别长度相同的相邻行
'''
def dfs(x):
    n=x-1
    cur_l = len(str(j[x]['级别']))
    next_l = len(str(j[n]['级别']))
    if cur_l==next_l:
        while cur_l==next_l: #x-1行起为子件集合
            n-=1
            next_l = len(str(j[n]['级别']))
        return j[n+1:x+1]
    else: # 独立，无相邻同级
        return [j[x]]

node_l = []
i=len(j)-1
while i >=0:
    res=dfs(i)
    l=len(res)
    node_l.append(l)
    i-=l
    print(i,l)
    if i>0:
        j[i]['_children']=res

# print(j[48])
# print(type(j))
res=[]
for i in range(len(j)):
    if j[i]['级别']==1:
        res.append(j[i])
print(res)