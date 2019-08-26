#coding=utf-8
import matplotlib.pyplot as plt
from matplotlib import animation  # 动图的核心函数

class Plot(object):
    """docstring for Plot"""
    def __init__(self, data):
        plt.rcParams['axes.unicode_minus'] = False
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 6))
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
                                  interval = 50,
                                  blit = False,
                                  repeat = False)
        # 不用imagemagick时，可以保存为html
        ani.save(save_path, writer = 'imagemagick', fps = 3) #

    def init(self):
        ax1 = self.ax1.pie([])
        ax2 = self.ax2.bar([], [])
        return (ax1, ax2)

    def update(self, i):
        self.ax1.cla()
        self.ax2.cla()
        labels = ['primary sector', 'secondary sector', 'tertiary sector']
        data = self.data[i]
        year = data[0]
        
        pie = self.ax1.pie(data[1], autopct='%1.1f%%',
                          startangle=90)
        self.ax1.legend(labels, ncol = len(labels), 
                        loc='lower left',  bbox_to_anchor=(-0.25, 1))
        bars = []
        for k in range(len(data[1])):
            bar = self.ax2.bar(k, data[1][k])
            bars.append(bar)
        #添加数据标签
        for rect in bars:
            rect = rect[0]
            h = rect.get_height()
            self.ax2.text(rect.get_x() + rect.get_width() / 2, h, '%d' % h, ha = 'center',va = 'bottom')
        self.ax2.set_ylabel('Unit: CNY 100 million')
        #隐藏横坐标
        self.ax2.set_xticks([])
        #设置title
        fig = self.fig.suptitle('China GDP composition by sector', fontsize=16, 
                          fontweight='bold')
        #添加时间
        self.ax1.text(-1, 1, str(year), fontsize=12, fontweight='bold', ha = 'center', va = 'top')
        return fig, (pie, bar)