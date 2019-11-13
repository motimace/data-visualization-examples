# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:33:52 2019

@author: bingo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#逐行读取数据
path = 'data/water_supply_and_use.csv'
def clean_data(path):
    #逐行读取数据
    with open(path) as f:
        lines = f.readlines()
    #选取部分转化为DataFrame    
    data = lines[2:18]
    data = pd.DataFrame(data)
    #替换换行符
    data = data.replace('\n', '', regex=True)
    #分割字符串
    data = data[0].str.split(',', expand=True)
    #设置columns
    data.columns = data.loc[0]
    #删除空行
    data.drop(0, inplace=True)
    #替换空白单元格
    data = data.replace('', np.nan, regex=True)
    #设置index
    data['时间'] = data['时间'].replace('年', '', regex=True).astype('int')
    data = data.set_index('时间')
    data = data.astype('float')
    return data

data = clean_data(path)

#pie gif
water = []
supply = data.columns[1:4]
use = data.columns[5:9]
for year in sorted(data.index[1:]):
    water.append([year, data.loc[year, supply].tolist(), 
                  data.loc[year, use].tolist()])

import sys
sys.path.append('../')

from module import plot_pie_gif
pie = plot_pie_gif.Plot(water)
pie.showGif('plots/water_pie.gif')

#supply water stack plot
supply = ['surface water', 'underground water', 'other']
use = ['agriculture water', 'industrial water', 'domestic water', 'ecological water']
fig, ax = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
ax[0].stackplot(data.index, data.iloc[:, 1:4].T, labels=supply, 
  colors=plt.get_cmap('Greens')([80, 100, 120]))
ax[0].set_ylabel('100 million steres')
ax[0].legend(bbox_to_anchor=(0.5, 1.1), loc='upper center', ncol=3)
ax[1].stackplot(data.index, data.iloc[:, 5:9].T, labels=use,
  colors=plt.get_cmap('Blues')([80, 100, 120, 140]))
ax[1].legend(bbox_to_anchor=(0.5, 1.15), loc='upper center', ncol=2)
title = fig.suptitle('China water supply and use', y=1.05, fontsize=16)
plt.savefig('plots/china-water-supply&use.jpg',
            bbox_inches='tight',bbox_extra_artists=[title])