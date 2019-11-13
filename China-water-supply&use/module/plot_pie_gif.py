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
                                  interval = 100,
                                  blit = False,
                                  repeat = False)
        # 不用imagemagick时，可以保存为html
        ani.save(save_path, writer = 'imagemagick', fps = 3) #

    def init(self):
        ax1 = self.ax1.pie([])
        ax2 = self.ax2.pie([])
        return (ax1, ax2)

    def update(self, i):
        self.ax1.cla()
        self.ax2.cla()
        supply_labels = ['surfce water', 'underground water', 'other']
        use_labels = ['agriculture water', ' industrial water', 'domestic water',
                      'ecological water']
        data = self.data[i]
        year = data[0]
        
        pie1 = self.ax1.pie(data[1], autopct='%1.1f%%',
                          startangle=90)
        self.ax1.legend(supply_labels, ncol = len(supply_labels), 
                        loc='lower left',  bbox_to_anchor=(0.1, -0.1))
        pie2 = self.ax2.pie(data[2], autopct='%1.1f%%',
                          startangle=90)
        self.ax2.legend(use_labels, ncol = 2, 
                        loc='lower left',  bbox_to_anchor=(0.1, -0.1))
        #设置title
        fig = self.fig.suptitle('China water supply and use in {:d}'.format(year), fontsize=16, 
                          fontweight='bold', y=0.9)
        #添加时间
        #self.ax1.text(-1, 1, str(year), fontsize=12, fontweight='bold', ha = 'center', va = 'top')
        return fig, (pie1, pie2)