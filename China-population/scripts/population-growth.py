# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 19:07:14 2019

@author: bingo
"""

import pandas as pd
import matplotlib.pyplot as plt

#逐行读取数据
path = 'data/population-growth.csv'
with open(path) as f:
    lines = f.readlines()
#选取部分转化为DataFrame    
rate_data = lines[2:6]
rate_data = pd.DataFrame(rate_data)
#替换换行符
rate_data = rate_data.replace('\n', '', regex=True)
#分割字符串
rate_data = rate_data[0].str.split(',', expand=True)
rate_data

#选取data中的数据部分，整理数据
rates = pd.DataFrame(rate_data.iloc[1:, 1:].T)
rates = rates.astype('float')
rates.info()

rate_data[0]
rates.columns = ['birth', 'death', 'growth']
rates['time'] = rate_data.iloc[0, 1:].replace('年', '', regex=True).astype('int')

rates.head()
#保存整理后的数据
rates.to_csv('data/population-growth-cleaned.csv', index=False)


"""读取整理后的数据"""
rates = pd.read_csv('data/population-growth-cleaned.csv')
#人口变化率
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 4),
                        sharey=True, tight_layout=True)
ax=axs[0]
ax.plot(rates['time'], rates['birth'])
ax.plot(rates['time'], rates['death'])
y1 = rates['birth']
y2 = rates['death']
ax.fill_between(rates['time'], y1, y2, where=y1 >= y2, alpha=0.5,
                facecolor='green', interpolate=True)
ax.fill_between(rates['time'], y1, y2, where=y1 <= y2, alpha=0.5,
                facecolor='red', interpolate=True)
ax.set_ylabel("change rate(%)")
ax.legend(loc='best')

ax = axs[1]
ax.plot(rates['time'], rates['growth'], 
              label='growth')
ax.legend(loc='upper right')

fig.suptitle('Natural growth rate of China population (1949~2018)', 
             y=1.05)
fig.savefig('plots/natural-growth-rate-of-china-population.jpg')
plt.show()