import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
import numpy as np
import math

class AET:
    def __init__(self):
        self.x = 0
        self.delta = 0
        self.ymax = 0
        self.next = None


def fillIn(x, y, pointnum, ax):
    #找出最大值
    yymax = 0
    for i in range(pointnum):
        if y[i] > yymax:
            yymax = y[i]
    #建立新边表NET空间
    NET = []
    for i in range(yymax):
        NET.append(AET())
    #建立新边表
    for i in range(0, yymax):
        for j in range(0, pointnum):
            #找到每个点的y坐标
            if y[j] == i:
                #这个点跟前面的一个点形成一条线段，跟后面的点也形成线段
                #存当前的x 到下一个点的detax 线段的最大y值
                if y[(j-1+pointnum)%pointnum] > y[j]:
                    AETpoint = AET()
                    AETpoint.x = x[j]
                    AETpoint.delta = (x[(j-1+pointnum)%pointnum]-x[j])/(y[(j-1+pointnum)%pointnum]-y[j])
                    AETpoint.ymax = y[(j-1+pointnum)%pointnum]
                    AETpoint.next = NET[i].next
                    NET[i].next = AETpoint
                if y[(j+1+pointnum)%pointnum] > y[j]:
                    AETpoint = AET()
                    AETpoint.x = x[j]
                    AETpoint.delta = (x[(j+1+pointnum)%pointnum]-x[j])/(y[(j+1+pointnum)%pointnum]-y[j])
                    AETpoint.ymax = y[(j+1+pointnum)%pointnum]
                    AETpoint.next = NET[i].next
                    NET[i].next = AETpoint
    #开始扫描
    AETable = AET()
    for i in range(yymax):
        #删除扫描线已经到达ymax的点（顶点不画）
        #不把它插入到AET扫描序列中去
        q = AETable
        p = AETable.next
        while p!=None:
            if p.ymax == i:
                q.next = p.next
                del p
                p = q.next
            else:
                q = q.next
                p = p.next
        #先对已经更新过值的AET表进行排序
        p = AETable.next
        head = AETable
        head.next = None
        while p!=None:
            while head.next!=None and p.x >= head.next.x:
                head = head.next
            temp = p.next
            p.next = head.next
            head.next = p
            p = temp
            head = AETable
        #插入当前NET表中的结点值
        p = NET[i].next
        q = AETable
        while p!=None:
            while (q.next!=None) and (p.x >= q.next.x):
                q = q.next
            temp = p.next
            p.next = q.next
            q.next = p
            p = temp
            q = AETable
        #画图
        p = AETable.next
        while p!=None and p.next!=None:
            start = math.floor(p.x+1)
            end = math.ceil(p.next.x)
            for x in range(start, end):
                ax.plot(x, i, 'r.')
            p = p.next.next
        #改写像素值，为下一次扫描做准备
        p = AETable.next
        while p!=None:
            p.x = p.x + p.delta
            p = p.next

if __name__ == '__main__':

    #初始化图标设置
    fig = plt.figure(figsize=(7, 7))
    ax = axisartist.Subplot(fig, 111, title='Fill Polygons');  
    fig.add_axes(ax)

    #输入点数(顺着输)，画多边形
    x = [int(n) for n in input('x:').split()]
    x.append(x[0])
    y = [int(n) for n in input('y:').split()]
    y.append(y[0])
    ax.plot(x, y)
    
    #填充多边形
    pointnum = len(x)
    fillIn(x, y, pointnum, ax)
    plt.axis("equal")
    plt.show()