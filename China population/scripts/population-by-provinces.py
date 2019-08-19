# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 15:31:36 2019

@author: bingo
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def clean_population():
    """整理国家统计局29省市年末常住人口数据"""
    provinces = ['黑龙江', '辽宁', '吉林', '河北', '山西', '河南', '山东', '江苏',
             '浙江', '上海', '湖北', '湖南', '安徽', '江西', '福建', '广东',
             '广西', '海南', '云南', '贵州', '重庆', '四川', '西藏', '新疆',
             '青海', '宁夏', '甘肃', '陕西', '内蒙古']
    population_29 = pd.DataFrame()
    population_29['time'] = np.arange(19) + 2000
    for province in provinces:
        path = 'data/29省市/' + province + '.csv'
        with open(path) as f:
            lines = f.readlines()
        popu = pd.DataFrame(lines[3:5])
        popu = popu.replace('\n', '', regex=True)
        popu = popu[0].str.split(',', expand=True)
        #数据转置与筛选（2000-2018）
        popu = popu.T.drop(0)
        popu = popu.loc[:19]
        #列名
        popu.columns = ['time', province]
        popu[province] = popu[province].astype('int')
        popu['time'] = popu['time'].replace('年', '', regex=True).astype('int')
        popu = popu.sort_values(by='time')
        #各省市数据聚合
        population_29 = pd.merge(population_29, popu, on='time')
        print(" %s 人口数据整理完毕!" % province)
    return population_29

population_29 = clean_population()

#整合北京、天津和港澳台人口数据
population_5 = pd.DataFrame()
population_5['time'] = np.arange(19) + 2000

for city in ['北京', '天津', '香港', '澳门', '台湾']:
    path = 'data/京津/' + city + '.csv'
    _ = pd.read_csv(path)
    _['time'] = _['time'].astype('int')
    _[city] = _[city].astype('int')
    population_5 = pd.merge(population_5, _, on='time')
    
#整合34个行政区2000-2018年末总人口数据
populations = pd.merge(population_29, population_5, on='time')
populations = populations.set_index('time')
#保存数据
populations.to_csv('data/population-by-province.csv', encoding='utf_8_sig')

"""再次运行时直接读取各省市人口数据"""
populations = pd.read_csv('data/population-by-province.csv', 
                          index_col='time')

#各省市人口可视化
from pyecharts.charts import Map
from pyecharts import options as opts

attr = populations.columns.values
for time in populations.index:
    values = populations.loc[time].values
    popu_map = Map()
    popu_map.add(str(time), [list(z) for z in zip(attr, values)],  maptype="china", 
                          is_map_symbol_show=False)
    popu_map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    popu_map.set_global_opts(
            title_opts=opts.TitleOpts(title="中国各省市人口"),
            visualmap_opts=opts.VisualMapOpts(max_=10000),
        )
    popu_map.render("plots/" + str(time) + ".html")
    
#动态展示各省市人口变化
sorted_pops = []
for year in range(2000, 2019):
    populations.sort_values(year, axis=1, inplace=True)
    sorted_pops.append([year, populations.loc[year].tolist(), 
                        populations.columns.tolist()])
        
import plot_population_by_province

plot = plot_population_by_province.Plot(sorted_pops)
plot.showGif('plots/population-by-province.gif')