# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 18:12:03 2019

@author: bingo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

#逐行读取数据
path = 'data/china-GDP.csv'
def clean_data(path):
    #逐行读取数据
    with open(path) as f:
        lines = f.readlines()
    #选取部分转化为DataFrame    
    data = lines[2:70]
    data = pd.DataFrame(data)
    #替换换行符
    data = data.replace('\n', '', regex=True)
    #分割字符串
    data = data[0].str.split(',', expand=True)
    #设置columns
    data.columns = data.loc[0]
    #删除空行
    data.drop(0, inplace=True)
    #设置index
    data['时间'] = data['时间'].replace('年', '', regex=True).astype('int')
    data = data.set_index('时间')
    data = data.astype('float')
    return data

data = clean_data(path)
#保存整理好的数据
data.to_csv('data/china-gdp-composition-by-sector.csv', index=True,
            encoding='utf_8_sig')
#各产业增加值柱状图
fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(data.index, data.iloc[:,2], label='primary sector')
ax.barh(data.index, data.iloc[:,3], left=data.iloc[:,2], 
        label='secondary sector')
ax.barh(data.index, data.iloc[:,4], left=data.iloc[:,2]+data.iloc[:,3], 
        label='tertiary sector')
ax.set_xscale('log')
ax.legend(loc='best')
ax.set_xlabel('亿元', FontProperties='SimHei')
fig.savefig('plots/barplot-of-china-gdp-composition-by-sector.jpg')
plt.show()

#各产业折线图
fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(data.index, data.iloc[:,2], label='primary sector')
ax.plot(data.index, data.iloc[:,3], label='secondary sector')
ax.plot(data.index, data.iloc[:,4], label='tertiary sector')
ax.set_yscale('log')
ax.legend(loc='best')
ax.set_ylabel('亿元', FontProperties='SimHei')
fig.savefig('plots/line-chart-of-china-gdp-composition-by-sector.jpg')
plt.show()

#堆叠图
labels = ['primary sector', 'secondary sector', 'tertiary sector']
fig, ax = plt.subplots(figsize=(10, 8))
ax.stackplot(data.index, data.iloc[:,2], data.iloc[:,3], data.iloc[:,4], 
             labels=labels)
ax.legend(loc='upper left')
ax.set_ylabel('亿元', FontProperties='SimHei')
fig.savefig('plots/stackplot-of-china-gdp-composition-by-sector.jpg')
plt.show()