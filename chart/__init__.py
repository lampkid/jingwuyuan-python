# -*- coding:utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from jingwuyuan import codec

import os

class Chart(object):

    def __init__(self):
        fontPath = os.path.dirname(__file__) + u'/fonts/1.ttf'
        self.font = fm.FontProperties(fname=fontPath)

        plt.figure(figsize=(8,4))

    def drawBar(self, dataList, xlabels, xname='', yname='', title='', color='y', barWidth=0.35, bottom=None):

        plt.clf()

        xlabels = [codec.codecText(xlabel) for xlabel in xlabels]
        xname = codec.codecText(xname)
        yname = codec.codecText(yname)
        title = codec.codecText(title)

        #fig, ax = plt.subplots()
        ax = plt.subplot(111)

        ind = np.arange(len(dataList))  # the x locations for the groups
        rects = ax.bar(ind, dataList, barWidth, color=color, bottom=bottom)

        ax.set_title(title, fontproperties=self.font, fontweight=900)
        ax.set_xticklabels(xlabels, fontproperties=self.font, fontsize=10)
        ax.set_xlabel(xname, fontproperties=self.font)
        ax.set_ylabel(yname, fontproperties=self.font)
        self.autolabel(ax, rects)
        ax.set_xticks(ind+barWidth*0.5)
        ax.set_ylim(0)

    def drawStackBar(self, array2D, xlabels, xname='', yname='', title='', color=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'], barWidth=0.35, legendLabels=None):

        plt.clf()

        plt.figure(figsize=(8,6))

        xlabels = [codec.codecText(xlabel) for xlabel in xlabels]
        xname = codec.codecText(xname)
        yname = codec.codecText(yname)
        title = codec.codecText(title)

        #fig, ax = plt.subplots()
        ax = plt.subplot(111)

        rows, cols = np.shape(array2D)
        xLocation = np.arange(cols)



        stackIndexes = range(rows)
        colIndexes = range(cols)
        rects = None

        handles = []
        defLegendLabels = []
        for rowIndex in stackIndexes:
            if rowIndex == 0:
                bottom = [0 for i in colIndexes]
            else:
                bottom = self.sumColData4array2D(array2D, rowIndex)

            if len(color) > rowIndex:
                barColor = color[rowIndex]
            else:
                barColor = '#7ed53d'
            rects = ax.bar(xLocation, array2D[rowIndex], barWidth, color=barColor, bottom=bottom)
            dataLabelY = [bottom[i] + 0.3 * array2D[rowIndex][i] for i in colIndexes]
            self.manualLabel(ax, rects, dataLabelY)

            handles.append(rects[0])
            defLegendLabels.append('stack%d' % rowIndex);

        dataLabelY = self.sumColData4array2D(array2D, rows)
        totalHeight = dataLabelY
        self.manualLabel(ax, rects, dataLabelY, totalHeight)

        # 设置全局，如x坐标、label等
        ax.set_title(title, fontproperties=self.font, fontweight=900)

        ax.set_xticklabels(xlabels, fontproperties=self.font, fontsize=10)

        ax.set_xlabel(xname, fontproperties=self.font)
        ax.set_ylabel(yname, fontproperties=self.font)

        ax.set_xticks(xLocation + barWidth*0.5)
        ax.set_ylim(0)
        if legendLabels is None:
            legendLabels = defLegendLabels
        ax.legend(tuple(handles), tuple(legendLabels), prop=self.font, fontsize=10, mode='expand', ncol=rows, frameon=False, framealpha=0.4)

    def drawPie(self, fracs, labels=None):
        plt.clf()

        ax = plt.subplot(111)

        max = 0
        for frac in fracs:
            if frac > max:
                max = frac

        explode = [0.1 if max == i else 0 for i in fracs]

        pie =  ax.pie(fracs, explode=explode, labels=labels,
            colors=('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'),
                autopct='%1.1f%%', pctdistance=0.6, shadow=True,
                    labeldistance=1.1, startangle=None, radius=None,
                        counterclock=True, wedgeprops=None, textprops=None,
                            center = (0, 0), frame = False)

        from pprint import pprint
        texts = pie[1]
        autotexts = pie[2]
        plt.setp(texts, fontproperties=self.font)
        plt.setp(autotexts, color='#ffffff')

    def sumColData4array2D(self, array2D, rowIndex):

        arr = array2D[:rowIndex]
        return map(sum, zip(*arr))


    def save(self, file):
        plt.savefig(file, dpi=100)

    def manualLabel(self, ax, rects, dataLabelY, height=None):

        index = 0
        for rect in rects:
            if len(dataLabelY) > index:
                labelY = dataLabelY[index]
            else:
                labelY = rect.get_height()

            if height:
                barHeight = height[index]
            else:
                barHeight = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., labelY, '%d' % barHeight,
                    ha='center', va='bottom')
            index += 1

    def autolabel(self, ax, rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, '%d' % int(height),
                    ha='center', va='bottom')



if __name__ == '__main__':

    dataList = (20, 36, 30, 35, 27)
    xlabels = ('第一', '第二', '第三', '第四', '第五')

    ct = Chart()
    ct.drawBar(dataList, xlabels)
    ct.save('demo-bar.png')

    array2D = [
        [1,2,3,4,9],
        [5,6,7,8,9],
        [9,10,11,12,9],
    ]

    ct.drawStackBar(array2D, xlabels)
    ct.save('demo-stackbar.png')

    ct.drawPie(dataList, xlabels)
    ct.save('demo-pie.png')



