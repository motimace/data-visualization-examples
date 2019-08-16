# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 15:52:39 2019

@author: bingo
"""

import pandas as pd
import matplotlib.pyplot as plt


#逐行读取数据
path = 'data/population.csv'
with open(path) as f:
    lines = f.readlines()
#选取部分转化为DataFrame    
data = lines[2:8]
data = pd.DataFrame(data)
#替换换行符
data = data.replace('\n', '', regex=True)
#分割字符串
data = data[0].str.split(',', expand=True)
data
#选取data中的数据部分，整理数据
population = pd.DataFrame(data.iloc[1:, 1:].T)
population = population.astype('int')
population.info()

data.iloc[1:, 0]
population.columns = ['total', 'male', 'female']
population['time'] = data.iloc[0, 1:].replace('年', '', regex=True).astype('int')

population.head()
#保存整理后的数据
population.to_csv('data/population-cleaned.csv', index=False)


"""读取整理后的数据"""
population = pd.read_csv('data/population-cleaned.csv')
#总人口与男/女人口折线图
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 4),
                        sharex=True, tight_layout=True)
ax = axs[0]
for x in ['total', 'male', 'female']:
    ax.plot(population['time'], population[x], 'o-', label=x, markersize=3)
ax.set_ylabel("populations(10K)")
ax.legend(loc='best')

ax=axs[1]
ax.stackplot(population['time'], population['male'], population['female'], 
              labels=['male', 'female'])
ax.legend(loc='upper left')

fig.suptitle('Population of China by gender (1949~2018)', y=1.05)
fig.savefig('plots/population-of-china-by-gender.jpg')
plt.show()

#总人口与城镇/乡村人口
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 4),
                        tight_layout=True)
ax = axs[0]
for x in ['total', 'urban', 'rural']:
    ax.plot(population['time'], population[x], 'o-', label=x, markersize=3)
ax.set_ylabel("populations(10K)")
ax.legend(loc='best')

ax=axs[1]
ax.stackplot(population['time'], population['urban'], population['rural'], 
              labels=['urban', 'rural'])
ax.legend(loc='upper left')

fig.suptitle('Urban and rural population of China (1949~2018)', y=1.05)
fig.savefig('plots/urban-and-rural-population-of-china.jpg')
plt.show()