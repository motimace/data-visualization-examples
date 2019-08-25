#coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import animation  # 动图的核心函数

class Plot(object):
    """docstring for Plot"""
    def __init__(self, data):
        # 中文显示
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12,6), sharey=True)
        self.fig = fig
        self.ax1 = ax1
        self.ax2 = ax2
        self.data = data

    def showGif(self, save_path):
        plt.cla()
        ani = animation.FuncAnimation(fig = self.fig,
                                func = self.update,
                                frames = len(self.data),
                                init_func = self.init,
                                interval = 20,
                                blit = False,
                                repeat = False)
        # 不用imagemagick时，可以保存为html
        ani.save(save_path, writer = 'imagemagick', fps = 3) #

    def init(self):
        bar1 = self.ax1.barh([], [], label='male')
        bar2 = self.ax2.barh([], [], color = 'r', label='female')
        bar = [bar1, bar2]
        return bar
   
    def update(self, i):
        self.ax1.cla()
        self.ax2.cla()
        data = self.data[i]
        year = data[0]
        male = data[1]
        female = data[2]
        age = data[3]
        
        bar1 = self.ax1.barh(age, male)
        bar2 = self.ax2.barh(age, female, color = 'r')	
        #设置Y轴
        self.ax1.yaxis.set_ticks_position('right')
        ticks = self.ax1.get_yticks()
        self.ax1.set_yticks(ticks)
        self.ax1.set_yticklabels(['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', 
                            '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', 
                            '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', 
                            '90-94', '95-'])
        #设置X轴
        self.ax1.invert_xaxis()
        self.ax1.set_xticks([0, 1000, 2000, 3000, 4000, 5000, 6000, 7000])
        self.ax1.set_xticklabels([0, 10, 20, 30, 40, 50, 60, 70])
        self.ax1.set_xlabel('million')
        self.ax2.set_xticks([0, 1000, 2000, 3000, 4000, 5000, 6000, 7000])
        self.ax2.set_xticklabels([0, 10, 20, 30, 40, 50, 60, 70])
        self.ax2.set_xlabel('million')
        #设置图例
        blue_patch = mpatches.Patch(color='blue', label='male')
        self.ax1.legend(handles=[blue_patch], loc='upper left')
        red_patch = mpatches.Patch(color='red', label='female')
        self.ax2.legend(handles=[red_patch], loc='upper right')
        self.fig.suptitle(str(year))
        bar = [bar1, bar2]
        return bar