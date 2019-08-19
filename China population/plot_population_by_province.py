#coding=utf-8
import matplotlib.pyplot as plt
from matplotlib import animation  # 动图的核心函数

class Plot(object):
    """docstring for Plot"""
    def __init__(self, data):
        # 中文显示
        #plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots(figsize = (6, 12))
        self.fig = fig
        self.ax = ax
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
        bar = self.ax.barh([], [])
        return bar

    def update(self, i):
        self.ax.cla()
        data = self.data[i]
        x = data[1]
        y = data[2]
        year = data[0]

        bars = []
        for k in range(len(x)):
            bar = self.ax.barh(k, x[k])
            bars.append(bar)
        #添加数据标签
        for rect in bars:
            rect = rect[0]
            w = rect.get_width()
            self.ax.text(w, rect.get_y() + rect.get_height() / 2, '%d' % w, ha = 'left',va = 'center')

        #设置XY轴
        self.ax.set_title('中国各省市年末人口/万' + '    ' + str(year), 
                          fontsize=20, fontweight='bold',
                          loc='left')
        self.ax.set_yticks(range(len(y)))
        self.ax.set_yticklabels(y)
        #self.ax.invert_yaxis()
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        #设置text
        """
        self.ax.text(9000, 2, str(year), fontsize=20, fontweight='bold', 
                     ha='right', va='baseline')
        """
        return bar