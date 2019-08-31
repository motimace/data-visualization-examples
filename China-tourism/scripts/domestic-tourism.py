# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:59:27 2019

@author: bingo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#逐行读取数据
path = 'data/domestic-tourism.csv'
def clean_data(path):
    #逐行读取数据
    with open(path) as f:
        lines = f.readlines()
    #选取部分转化为DataFrame    
    data = lines[2:28]
    data = pd.DataFrame(data)
    #替换换行符
    data = data.replace('\n', '', regex=True)
    #分割字符串
    data = data[0].str.split(',', expand=True)
    #设置columns
    data.columns = data.loc[0]
    #删除首行
    data.drop(0, inplace=True)
    #设置index
    data['时间'] = data['时间'].replace('年', '', regex=True).astype('int')
    data = data.set_index('时间')
    #替换空白，移除空行
    data = data.replace('', np.nan)
    data.dropna(how='all', inplace=True)
    #数值格式
    data = data.astype('float')
    return data

data = clean_data(path)

urban_residents = data['城镇居民国内游客(百万人次)']
rural_residents = data['农村居民国内游客(百万人次)']

urban_cost = data['城镇居民国内旅游总花费(亿元)']
rural_cost = data['农村居民国内旅游总花费(亿元)']

#城镇居民和农村居民国内游客对比
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))
ax1.barh(data.index, urban_residents, label='urban')
ax1.barh(data.index, rural_residents, left=urban_residents, 
        label='rural')
ax1.legend(loc='best')
ax1.set_xlabel('million')
ax1.set_title('Domestic tourist arrivals: Urban VS rural residents')
ax2.barh(data.index, urban_cost, label='urban')
ax2.barh(data.index, rural_cost, left=urban_cost, label='rural')
ax2.legend(loc='best')
ax2.set_xlabel('CNY 100 Million')
ax2.set_title('Domestic travel spending: Urban VS rural residents')
fig.savefig('plots/domestic-tourism.jpg')
plt.show()