# -*- coding:utf-8 -*-
"""
道格拉斯算法的实现
程序需要安装shapely模块
"""
import math
from shapely import wkt, geometry
import matplotlib.pyplot as plt
 
 
class Point:
    """点类"""
    x = 0.0
    y = 0.0
    index = 0  # 点在线上的索引
 
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index
 
 
class Douglas:
    """道格拉斯算法类"""
    points = []
    D = 100  # 容差
 
    def readPoint(self, map = None):
        """生成点要素"""
        if map == None:
            g = [(1,4),(2,3),(3, 5),(4,2),(6,4),(8,4),(9,5),(12, 4),(15 ,8),(12, 10),(9, 9),(8, 10),(7, 8),(6, 11),(5, 12),(4, 10),(3, 11),(1, 4)]
        else:
            g = map
        for i in range(len(g)):
            self.points.append(Point(g[i][0], g[i][1], i))
 
    def compress(self, p1, p2):
        """具体的抽稀算法"""
        swichvalue = False


        # 一般式直线方程系数 A*x+B*y+C=0,利用点斜式,分母可以省略约区
        # A=(p1.y-p2.y)/math.sqrt(math.pow(p1.y-p2.y,2)+math.pow(p1.x-p2.x,2))
        A = (p1.y - p2.y)
        # B=(p2.x-p1.x)/math.sqrt(math.pow(p1.y-p2.y,2)+math.pow(p1.x-p2.x,2))
        B = (p2.x - p1.x)
        # C=(p1.x*p2.y-p2.x*p1.y)/math.sqrt(math.pow(p1.y-p2.y,2)+math.pow(p1.x-p2.x,2))
        C = (p1.x * p2.y - p2.x * p1.y)
 
        m = self.points.index(p1)
        n = self.points.index(p2)
        distance = {}
        middle = None
 
        if (n == m + 1):
            return
        # 计算中间点到直线的距离
        for i in range(m + 1, n):
            d = abs(A * self.points[i].x + B * self.points[i].y + C) / math.sqrt(math.pow(A, 2) + math.pow(B, 2))
            distance[i] = d
 
        dmax_index = max(distance, key=distance.get)
        dmax = distance[dmax_index]
 
        if dmax > self.D:
            swichvalue = True
        else:
            swichvalue = False
 
        if (not swichvalue):
            i = m+1
            while i != n:
                del self.points[i]
                n = n - 1
        else:
            middle = self.points[dmax_index]
            self.compress(p1, middle)
            self.compress(middle, p2)
 
    def printPoint(self):
        """打印数据点"""
        for p in self.points:
            print("%d,%f,%f" % (p.index, p.x, p.y))
 
 
import json

# 加载GeoJSON文件
with open('USA.geo.json', 'r') as f:
    geojson_data = json.load(f)

# 提取坐标
def extract_coordinates(geojson):
    coordinates = []
    if 'features' in geojson:
        for feature in geojson['features']:
            if 'geometry' in feature and 'coordinates' in feature['geometry']:
                coordinates.append(feature['geometry']['coordinates'])
    return coordinates

coordinates = extract_coordinates(geojson_data)

# 输出坐标
for coord in coordinates:
    print(type(coord))
    print(coord)

coord = coordinates[0]

map = coord[5][0]

map_int = [[int(value * 100) for value in sublist] for sublist in map]

original_edges = len(map) - 1

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 假设Douglas和map已经定义并正确读取了点数据
d = Douglas()
d.readPoint(map=map_int)

fig, (a1, a2) = plt.subplots(1, 2)

dx = [p.x for p in d.points]
dy = [p.y for p in d.points]

a1.plot(dx, dy, color='g', linestyle='-', marker='+')
p1 = d.points[0]
p2 = d.points[-2]
d.compress(p1, p2)

dx1 = [p.x for p in d.points]
dy1 = [p.y for p in d.points]


a2.plot(dx1, dy1, color='r', linestyle='-', marker='+')

# 设置图像的交互模式
fig.canvas.mpl_connect('scroll_event', lambda event: zoom(event, fig))

def zoom(event, fig):
    ax = event.inaxes
    if ax is None:
        return

    scale_factor = 1.1 if event.button == 'up' else 0.9

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    new_xlim = [(x - ax.get_xlim_center()) * scale_factor + ax.get_xlim_center() for x in xlim]
    new_ylim = [(y - ax.get_ylim_center()) * scale_factor + ax.get_ylim_center() for y in ylim]

    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)
    fig.canvas.draw_idle()

plt.show()

edges = len(d.points) - 1

print(f"原来的边数:{original_edges}\n处理后的边数:{edges}")