# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib_inline.config import InlineBackend
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


"""
Visualization of user gender proportion
"""


plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
filename = 'fans_data.csv'
with open(filename, encoding='utf-8') as f:
    reader = csv.reader(f)
    header_row = next(reader)

    gender = []
    for row in reader:
        sex = row[8]
        gender.append(sex)

    man = 0
    woman = 0
    others = 0
    # 统计男女比例
    for sex in gender:  # 从XB列读取数据
        if sex == 'm':
            man += 1
        elif sex == 'f':
            woman += 1


    # 绘制饼状图

    labels = ['男', '女']
    # 绘图显示的标签
    values = [man, woman]
    colors = ['lightcyan', 'lightcoral']
    #explode = [0, 0.1]
    # 旋转角度
    plt.title("长津湖关注者男女比例", fontsize=20)
    # 标题
    plt.pie(values, labels=labels,  colors=colors,
            startangle=180,
            shadow=True, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()
