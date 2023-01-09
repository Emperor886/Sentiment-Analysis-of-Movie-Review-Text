# -*- coding:utf-8 -*-
from pyecharts.charts import Map
from pyecharts import options as opts
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
Draw a regional heat map
"""

plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['kaiti']

# df = pd.read_csv(filename, encoding='gb18030')
df = pd.read_excel('cjh_weibo.xlsx')
df['loc'] = df['loc'].astype(str).apply(lambda x: x.split(' ')[0])
df = df[~df['loc'].isin(['其他'])]  # df['loc'] = df['loc'].fillna('未知')
# df=df[~df['loc'].isin('')]
loc = pd.DataFrame(df['loc'].value_counts())
print(loc.head())
city = np.char.rstrip(list(loc.index))
city_num = [(k, v) for k, v in zip(city, loc['loc'])]
length = len(city_num)
map1 = Map(init_opts=opts.InitOpts(width="1200px", height="800px"))
map1.set_global_opts(
    title_opts=opts.TitleOpts(title="长津湖关注者地区分布"),
    visualmap_opts=opts.VisualMapOpts(max_=city_num[0][1], is_piecewise=True,  # 最大值由 max_设置
                                      pieces=[
                                          {"max": city_num[0][1] + 1, "min": city_num[-int(length / 4 * 3)][1] + 1,
                                           "label": "top 25%", "color": "#754F44"},
                                          {"max": city_num[-int(length / 4 * 3)][1],
                                           "min": city_num[-int(length / 2)][1] + 1, "label": "top 50%",
                                           "color": "#EC7357"},
                                          {"max": city_num[-int(length / 2)][1],
                                           "min": city_num[-int(length // 4)][1] + 1, "label": "bottom 50%",
                                           "color": "#FDD692"},
                                          {"max": city_num[-int(length // 4)][1], "min": city_num[-1][1] + 1,
                                           "label": "bottom 25%", "color": "#FBFFB9"},
                                          {"max": city_num[-1][1], "min": 0, "label": "very few", "color": "#FFFFFF"},
                                      ]))  # 最大数据范围，分段
map1.add("", [list(z) for z in zip(city, loc['loc'])], maptype='china', is_roam=False,
         is_map_symbol_show=False)
map1.render('fans_loc.html')
