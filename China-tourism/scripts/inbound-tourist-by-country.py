# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 16:30:45 2019

@author: bingo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#逐行读取数据
path = 'data/inbound-tourist-by-country.csv'
def clean_data(path):
    #逐行读取数据
    with open(path) as f:
        lines = f.readlines()
    #选取部分转化为DataFrame    
    data = lines[2:32]
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

#入境游客折线图
plt.plot(data.index, data.iloc[:,0])
plt.show()
plt.bar(data.index, data.iloc[:,0])
plt.show()

asia = data['亚洲入境游客(万人次)']
europe = data['欧洲入境游客(万人次)']
africa = data['非洲入境游客(万人次)']
north_america = data['北美洲入境游客(万人次)']
latin_america = data['拉丁美洲入境游客(万人次)']
oceania = data['大洋洲及太平洋岛屿入境游客(万人次)']
labels = ['Asis', 'Africa', 'Europe', 'North America', 
          'Latin American', 'Oceania']

continents = [asia, africa, europe, north_america, latin_america, oceania]
#折线图
for continent, label in zip(continents, labels):
    plt.plot(data.index, continent, label=label)
plt.legend(loc='best')
plt.ylabel('10K')
plt.title('China inbound tourist by continent')
plt.savefig('plots/line-chart-of-china-inbound-tourist-by-continent.jpg')
plt.show()

#堆叠图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
ax1.stackplot(data.index, asia, europe, north_america,
              labels=['Asia', 'Europe', 'North America'])
ax1.legend(loc='upper left')
ax1.set_ylabel('10K')
ax2.stackplot(data.index, africa, latin_america, oceania,
              labels=['Africa', 'Latin America', 'Oceania'])
ax2.legend(loc='upper left')
ax2.set_ylabel('10K')
fig.savefig('plots/stackplot-of-china-inbound-tourist-by-continent.jpg')
plt.show()