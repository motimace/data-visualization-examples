# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 16:22:45 2019

@author: bingo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_data(path):
    #逐行读取数据
    with open(path) as f:
        lines = f.readlines()
    #选取部分转化为DataFrame    
    data = lines[2:17]
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


path_male = 'data/male-population-sample-survey-by-age.csv'
path_female = 'data/female-population-sample-survey-by-age.csv'

male = clean_data(path_male)
female = clean_data(path_female)
#读取总人口数据
total = pd.read_csv('data/population_cleaned.csv', index_col='time')
total = total['total'].loc[male.index]
#根据抽样调查计算各年龄段人数
male_total = male.iloc[:, 1:].div(male.iloc[:,0]+female.iloc[:,0], axis=0)
male_total = male_total.mul(total, axis=0)

female_total = female.iloc[:, 1:].div(male.iloc[:,0]+female.iloc[:,0], axis=0)
female_total = female_total.mul(total, axis=0)
#输出数据
male_total.to_csv('data/male-population-by-age.csv', 
                  index=True, encoding='utf_8_sig')
female_total.to_csv('data/female-population-by-age.csv', 
                  index=True, encoding='utf_8_sig')

"""重新读取数据"""
male_total = pd.read_csv('data/male-population-by-age.csv', index_col='时间')
female_total = pd.read_csv('data/female-population-by-age.csv', index_col='时间')
#封装为类
data = []
for year in sorted(male_total.index.values):
    data.append([year, male_total.loc[year], 
                 female_total.loc[year], male_total.columns])

from PlotUtil import Plot
plot = Plot(data)
plot.showGif('plots/population-structure.gif')