#!/usr/bin/env python
#-*- coding:utf8 -*-

# TODO: pandas 本身的 plot 就挺好用!!!!


# 基本框架 BEGIN ----------------------------------------
# matplotlib的基本的组件的定义:
# https://matplotlib.org/tutorials/introductory/usage.html
# 基本框架 END   ----------------------------------------


# 知道你可以画什么
# 1) https://python-graph-gallery.com
# 2) seaborn本来的gallary

# interactive: https://blog.dominodatalab.com/interactive-dashboards-in-jupyter/
# you must install this extension https://github.com/jupyter-widgets/ipywidgets
# 可能会遇到这个错误  Widget Javascript not detected.  It may not be installed or enabled properly
# 最终没有解决


# https://stackoverflow.com/questions/37604289/tkinter-tclerror-no-display-name-and-no-display-environment-variable
# 在terminal里画图会报错 _tkinter.TclError: no display name and no $DISPLAY environment variable
# 必须加下面来防止出错
import matplotlib
matplotlib.use('Agg')
# plt.clf()  # 清理之前的内容。好像plt.savefig和plt.show()不一样，似乎有时候不会清理之前的内容
plt.savefig('filename.png', bbox_inches='tight')  # use this instead of plt.show()
#  bbox_inches='tight' 的效果非常赞，它可以让两边边变窄， 周围的文字留全！！！！

%matplotlib inline  # 这个可以保证不用 plt.show() 也能出现图


# 中文显示:
# 需要自己下载字体 anaconda3/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
# 还得删除缓存：https://www.zhihu.com/question/25404709/answer/309784195
# 这个缓存是用户相关的，只会影响自己的用户
from matplotlib.font_manager import _rebuild
_rebuild() #reload一下



# 如果pandas希望在jupyter里display所有的列，那么用下面的代码
# https://stackoverflow.com/questions/11361985/output-data-from-all-columns-in-a-dataframe-in-pandas
pd.set_option('display.max_columns', None)
# 如果希望显示pandas cell内部的所有内容:
# https://stackoverflow.com/questions/25351968/how-to-display-full-non-truncated-dataframe-information-in-html-when-convertin
pd.set_option('display.max_colwidth', -1)


# control the font size
# https://stackoverflow.com/a/39566040
import matplotlib.pyplot as plt

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# 如果想一次改变所有的font size;  这个是一个全局性的，会持续生效
matplotlib.rcParams.update({'font.size': 14})



import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def multi_plot_like_grid(n):
    '''
    我的另外一个目的是五脏俱全， 各种通用的小功能在我这里都能看到
    '''
    fig, axes = plt.subplots(2, 2, figsize=(12,4)) # Unknown size unit.

    axes = axes.flatten() #  If we dont't flatten this, we have to use axes[0, 1] to select the table.

    axes[0].hist(n, bins=29)
    axes[0].set_title("Default histogram")
    axes[0].set_xlim((min(n), max(n)))

    # this can be replaced by the function below.
    # axes[0].xaxis.set_label_text('Number of sectors with big loss in a day')
    # axes[0].yaxis.set_label_text('Number of days with that number of sectors big loss')

    fontsize = 20  # search fontsize for all font size related code
    axes[0].set_xlabel("xlabel", fontsize=fontsize)
    axes[0].set_ylabel("ylabel", fontsize=fontsize)

    axes.axvline(x=np.median(n), color='g', label='median') # set label
    axes.axvline(x=np.mean(n), color='r', label='mean')

    axes[1].hist(n, cumulative=True, bins=29)
    axes[1].set_title("Cumulative detailed histogram")
    axes[1].set_xlim((min(n), max(n)));


    plt.legend(fontsize=fontsize) # show label
    plt.yticks(fontsize=fontsize)
    plt.xticks(rotation=45, fontsize=fontsize)  # set a rotation for label
    plt.show()

import matplotlib.dates as mdates
from datetime import datetime

# 如果想实现坐标显示时间，可以直接用 datetime64 这个类型就好
# map(pendulum.parse, data) 会有问题,得到的类型不是datetime64.
# 用下面的可以从string得到datetime64这个类型
pd.Series(play_df.TradeDate.unique()).apply(pendulum.parse)

def plot(x, data, year_start, year_end):
    '''
    plot histgram to control the details.
    '''
    dates = []
    for i in xrange(x, 30):
        dates.extend(list(data[i]))
    date_nums = [mdates.date2num(datetime.strptime(d, '%Y-%m-%d')) for d in dates]
    min_date, max_date = min(date_nums), max(date_nums)

    fig, axes = plt.subplots(1, 1, figsize=(25, 5)) # Unkown size
    axes.set_title("The number of days in a month with more than `x - 1` loss")

    bin_num = (year_end - year_start) * 12
    start_num = mdates.date2num(datetime(year_start, 1, 1))
    end_num = mdates.date2num(datetime(year_end, 1, 1))
    span = (end_num - start_num) * 1. / bin_num
    bins = np.linspace(start_num, end_num, bin_num + 1)
    bins  = [num for num in bins if  min_date - span <= num <= max_date + span]

    axes.hist(date_nums, bins=bins)
    # axes.hist(date_nums, bins=12 * 9)  # only numbers are ok.
    # axes.hist(date_nums, bins= "auto")  #  auto will be also ok In most times.

    # Auto will be ok in most times.
    # locator = mdates.AutoDateLocator()
    # axes.xaxis.set_major_locator(locator)
    # axes.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))

    axes.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m'))

    axes.xaxis.set_label_text('Date')
    axes.yaxis.set_label_text('Freq')
    plt.show()


def set_x_labels_manully():
    x = np.arange(2,10,2)
    y = x.copy()
    x_ticks_labels = ['jan','feb','mar','apr','may']

    fig, ax = plt.subplots(1,1)
    ax.plot(x,y, '-', lw=1.)  # line weight will how much the line weights. Less than 1. will make it transparent
    # Set number of ticks for x-axis
    ax.set_xticks(x)
    # Set ticks labels for x-axis
    ax.set_xticklabels(x_ticks_labels, rotation='vertical', fontsize=18)
    plt.show()




def plot_two_yaxes():
    fontsz = 40
    fig, axes = plt.subplots(1, 1, figsize=(20, 12))

    # This must run before defining twinx but after defining  axes to take effect
    plt.xticks(rotation=45)

    x = np.linspace(0.0001, 1, 100)
    right_axes = axes.twinx()
    right_axes.grid(False)  # Only the first shows grid.
    for tickset in [axes.xaxis.get_major_ticks(), axes.yaxis.get_major_ticks(),
					right_axes.xaxis.get_major_ticks(), right_axes.yaxis.get_major_ticks()]:
	for tick in tickset:
		tick.label.set_fontsize(fontsz)
    axes.plot(x, np.exp(x), ls='--',label='exp')
    right_axes.plot(x, np.log(x), ls=':', label='log')
    h1, l1 = axes.get_legend_handles_labels()
    h2, l2 = right_axes.get_legend_handles_labels()

    axes.set_xlabel("X", fontsize=fontsz)
    axes.set_ylabel("Y", fontsize=fontsz)
    right_axes.set_ylabel("YY", fontsize=fontsz)
    plt.legend(h1+h2, l1+l2, fontsize=fontsz)
    plt.yticks(fontsize=fontsz)  # this will decide the right axes
    plt.show()


def plot_three_yaxes():
    fontsz = 40
    fig, axes = plt.subplots(1, 1, figsize=(20, 12))

    # This must run before defining twinx but after defining  axes to take effect
    plt.xticks(rotation=45)

    x = np.linspace(0.0001, 1, 100)
    right_axes = axes.twinx()
    right_axes.grid(False)  # Only the first shows grid.
    plt.yticks(fontsize=fontsz) # this will decide the ticks fontsize of right_axes

    right_axes2 = axes.twinx()
    right_axes2.grid(False)  # Only the first shows grid.
    for tickset in [axes.xaxis.get_major_ticks(), axes.yaxis.get_major_ticks(),
                    right_axes.xaxis.get_major_ticks(), right_axes.yaxis.get_major_ticks(),
                    right_axes2.xaxis.get_major_ticks(), right_axes2.yaxis.get_major_ticks(),]:
        for tick in tickset:
            tick.label.set_fontsize(fontsz)
    axes.plot(x, np.exp(x), ls='--',label='exp')
    right_axes.plot(x, np.log(x), ls=':', label='log')
    right_axes2.plot(x, x, ls='-', label='linear')

    right_axes2.spines['right'].set_position(('outward', 120))

    h1, l1 = axes.get_legend_handles_labels()
    h2, l2 = right_axes.get_legend_handles_labels()
    h3, l3 = right_axes2.get_legend_handles_labels()

    axes.set_xlabel("X", fontsize=fontsz)
    axes.set_ylabel("Y", fontsize=fontsz)
    right_axes.set_ylabel("YY", fontsize=fontsz)
    right_axes2.set_ylabel("YYY", fontsize=fontsz)

    plt.legend(h1+h2+h3, l1+l2+l3, fontsize=fontsz)
    plt.yticks(fontsize=fontsz)  # this will decide the font size of right_axes2
    plt.show()


# seaborn related BEGIN --------------------------------------------------

# 可以用seaborn来画heatmap， 但是最后得自己加上plot.show()
## DOC: http://seaborn.pydata.org/generated/seaborn.clustermap.html
## convert data to DataFrame for setting row keys and column headers
import pandas as pd
dataframe = pd.DataFrame(data=feature_array,
            index=[k[0] for k in train_keys+test_keys], columns=column_list)
## 参考:https://stackoverflow.com/questions/20763012/creating-a-pandas-dataframe-from-a-numpy-array-how-do-i-specify-the-index-colum

# We can filter the rows. Filtered_index can be an boolean array or integer array
filtered_dataframe = dataframe.iloc[filtered_index]

import matplotlib.pyplot as plt
import seaborn as sns; sns.set(color_codes=True)


# seaborn 设置figure size
sns.set(rc={'figure.figsize':(10,10)})

# color是一个字符串表示的 (n,) 的 dataframe, 它有自己的index
fd_len = filtered_dataframe.shape[0]
str_colors = ["#%02x%02x%02x" % tuple((np.array(color) * 255).astype(np.int)) for color in sns.color_palette("Blues", fd_len)]
# row_colors 是一个data frame
row_colors=pd.DataFrame(data=str_colors, index=filtered_dataframe.index)
# {row,col}_cluster: 设置是否要对行或者列做cluster
g = sns.clustermap(filtered_dataframe, row_cluster=False, row_colors=row_colors, figsize=(24, 24))
## 返回值是:  A ClusterGrid instance.
plt.show()

# 如果想提取其中的类:  https://stackoverflow.com/questions/27924813/extracting-clusters-from-seaborn-clustermap
from scipy.cluster import hierarchy
from scipy.spatial import distance
row_linkage = hierarchy.linkage(
            distance.pdist(dataframe), method='average')
sns.clustermap(dataframe, row_linkage=row_linkage, figsize=(24, 24))
plt.show()

def merge_linkage(linkage, cluster_n):
    total_n = len(linkage) + 1  # there are `totoal_n` leaves
    new_cluster_i = total_n
    cluster_set_map = {}
    for i in range(total_n):
        cluster_set_map[i] = set([i])
    for clst1, clst2, diff, cls_n in linkage[:-cluster_n + 1]:
        # print clst1, clst2, diff, cls_n, new_cluster_i
        clst1, clst2, cls_n = int(clst1), int(clst2), int(cls_n)
        cluster_set_map[new_cluster_i] = cluster_set_map[clst1] | cluster_set_map[clst2]
        assert(len(cluster_set_map[new_cluster_i]) == cls_n)
        del cluster_set_map[clst1]
        del cluster_set_map[clst2]
        new_cluster_i += 1
    return cluster_set_map


def get_clusters(cluster_set_map):
    '''
    Get an Object like what sklearn.cluster.XXXX.fit returns
    '''
    total_n = np.sum([len(cids) for cids in cluster_set_map.values()])
    labels = np.full((total_n,), -1)
    for i, cids in enumerate(cluster_set_map.values()):
        labels[list(cids)] = i
    clusters = lambda: None
    clusters.labels_ = labels
    return clusters


# show heatmap with color selected
# https://seaborn.pydata.org/generated/seaborn.diverging_palette.html#seaborn.diverging_palette
# h_neg, h_pos 代表正负的颜色
# jupyter可以通过这种方式获得合适的 sns.choose_diverging_palette()
cmap = sns.diverging_palette(10, 150, sep=20, as_cmap=True, center='light')
sns.heatmap(data, linewidths=1, cmap=cmap)
plt.show()
# NOTE： 如果想让0对齐到无色，请设置 vmax 和 vmin !!!!!!



# seaborn 实现 stack=True的效果
# https://stackoverflow.com/questions/22787209/how-to-have-clusters-of-stacked-bars-with-python-pandas
# 普通的这么画就可以  https://python-graph-gallery.com/13-percent-stacked-barplot/

# seaborn 有很多 pyplot的替代但是信息更丰富的图像, 而且文档也更好;
# 这里有各种全面的example. https://seaborn.pydata.org/examples/index.html
sns.distplot(x, rug=True) # 替代histplot, https://seaborn.pydata.org/generated/seaborn.distplot.html
# rug is really a good function to check the distribution of the data

# NOTE: seaborn的图像分类,  https://zhuanlan.zhihu.com/p/27683042

# Barplot的最小单位是一组值，用一个柱状图和一个误差线来描述。
sns.barplot(x='type', y=iname, data=df) # 需要画误差线时用这个工具 https://seaborn.pydata.org/generated/seaborn.barplot.html
# x will be a attribute to describe the x class
# y will be the value in that class。
# ci default value is 'sd', the stand variable will be there

sns.tsplot # 用来画时间轴


# 如果一个图中有多个axes， 需要单独对axes做操作, 做下面的操作。
g = sns.XXXXX
for i, ax in enumerate(g.fig.axes):   ## getting all axes of the fig object
     ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

sns.countplot # https://seaborn.pydata.org/generated/seaborn.countplot.html



# seaborn通用参数
plot_kws={
    "s": 3, # marker的大小
    'alpha': 0.5, # 50%透明度
}


# seaborn 之外的api操作图像
# seaborn 可以通过 ax做各种操作
# 常用: set_title, set_xlim, plt.subtitle
# **kwargs 可以传入各种参数:
# 常用: s(控制marker的size)


# seaborn related END    --------------------------------------------------


# share the same x and y
# http://matplotlib.org/examples/pylab_examples/shared_axis_demo.html
# set the figure size at the same time https://stackoverflow.com/questions/10388462/matplotlib-different-size-subplots
# 注意subplot必须要设置subplot(nrows, ncols, plot_number) 参数！！！

import matplotlib.pyplot as plt
import numpy as np
def share_x_y():
    t = np.arange(0.01, 5.0, 0.01)
    s1 = np.sin(2*np.pi*t)
    s2 = np.exp(-t)
    s3 = np.sin(4*np.pi*t)

    fig = plt.figure(figsize=(12, 6))

    ax1 = plt.subplot(2, 1, 1)
    ax1.scatter(t, s1)
    ax1.set_facecolor((0.9, 0.9, 0.9))  # change the color of this axes

    # share x and y
    ax2 = plt.subplot(2, 1, 2, sharex=ax1, sharey=ax1)
    ax2.scatter(t, s3)

    plt.show()


# 搜索 get_x， 这个方法没有下面的方法方便
def auto_label(bar_ret, axes=None, color='k'):
    if axes is None:
        axes = plt
    for rect in bar_ret:
        height = rect.get_height()
        axes.text(rect.get_x() + rect.get_width()/2., 1.01 * height,
                '%.03f' % height,
                ha='center', va='bottom', rotation='vertical', color=color)

# Plot multiple bar
def plot_multi_bars():
    '''
    How to set text on bar:How to set text on bar:  https://matplotlib.org/examples/api/barchart_demo.html
    '''
    N = 10
    fig = plt.figure(figsize=(20, 10))
    GROUP_N = 3.
    width = 0.9 / GROUP_N
    xticks_n = np.arange(N)
    xticks_label = ['label%d' % i for i in range(N)]

    data = np.random.rand(GROUP_N, 10)


    plt.title("Data")
    auto_label(plt.bar(xticks_n - width, data[0], width=width, label='data1'))
    auto_label(plt.bar(xticks_n, data[1], width=width, label='data2'))
    auto_label(plt.bar(xticks_n + width, data[2], width=width, label='data3'))

    #  If multi axes is needed in one plot. This must run before defining twinx but after defining axes.
    plt.xticks(xticks_n, xticks_label, rotation='vertical')
    plt.legend()
    plt.show()

# Plot multiple bar
def plot_multi_bars_with_sns():
    '''
    '''
    N = 10
    GROUP_N = 3
    labels = ['label%d' % i for i in range(N)]
    data = np.random.rand(GROUP_N, 10).reshape(-1)

    df = pd.DataFrame(dict(data=data, label=labels * GROUP_N, group=['g1', 'g2', 'g3'] * N))
    sns.factorplot(data=df,  x='label', y='data', hue='group', kind='bar')
    # Hue 代表x轴每个值 再分成小类别显示
    plt.xticks(rotation='vertical')
    plt.show()


# format y plot.  https://stackoverflow.com/questions/31357611/format-y-axis-as-percent
# percentage example
vals = ax.get_yticks()
ax.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])


# stack plot
# example 1): https://python-graph-gallery.com/251-stacked-area-chart-with-seaborn-style/
# example 2): https://matplotlib.org/gallery/lines_bars_and_markers/stackplot_demo.html



# 加文字篇 https://stackoverflow.com/a/25449186
# ax = df.plot(kind='bar') 时，  可以直接通过这种方式加文字
# 如果是 barh时， 需要把下面的 get_x 换成 get_y， 把 get_height换成get_width.
# 我理解这里的get_x是图中柱状图根部的位置， height width指的是柱状图本身的形状
for p in ax.patches:
	ax.annotate("%.4f" % p.get_height(), (p.get_x() * 1.01, p.get_height() * 1.01)
# 我觉得这里的 1.01 常常不要也行

# 顺便控制一下bar的高度
heights = [p.get_height() for p in ax.patches]
max_h, min_h = max(heights), min(heights)
delta = max_h - min_h
pct = 0.8
margin = delta * (1. - pct) / 2
ax.set_ylim(max_h + margin, min_h - margin)

ax.invert_yaxis()  # 需要的话， 让它从上往下排列

# 来一版 barh的
ax = methods_perf.plot(kind='barh')
for p in ax.patches:
     ax.annotate("%.4f" % p.get_width(), (p.get_width(), p.get_y()))
widths = [p.get_width() for p in ax.patches]
max_w, min_w = max(widths), min(widths)
delta = max_w - min_w
pct = 0.8
margin = delta * (1. - pct) / 2
ax.set_xlim(min_w - margin, max_w + margin)




# Pandas .plot篇  BEGIN --------------------------------
# 控制subplots
df.plot(subplots=True, layout=(3, 3), figsize=(10, 10), sharey=True)
# Pandas .plot篇  END   --------------------------------



# Subplots篇 BEGIN -------------------------------------------------
# subplots 之间的距离
# 这个对pandas的plot也有效
# 省事直接用 fig.tight_layout() https://stackoverflow.com/questions/6541123/improve-subplot-size-spacing-with-many-subplots-in-matplotlib
# 没用再
plt.subplots_adjust(
    left = 0.125,  # the left side of the subplots of the figure
    right = 0.9,    # the right side of the subplots of the figure
    bottom = 0.1,   # the bottom of the subplots of the figure
    top = 0.9,      # the top of the subplots of the figure
    # 上面几个参数有时候越大靠得越近，下面的几个参数一般会按期望来
    wspace = 0.2,   # the amount of width reserved for blank space between subplots
    hspace = 0.2,   # the amount of height reserved for white space between subplots)
)

# 进一步微调某个ax的距离
pos2 = ax.get_position()
pos2.x0 -= 0.02
pos2.x1 -= 0.02
pos2.y1 -= 0.05  # 这个是负值的时候， 图片的上边界会往下缩
ax.set_position(pos2)
# x0 代表： . y0 代表.
# x1 代表： . y1 代表.


# 样式
df.plot(
    style=['.'] * 4,  # 每个曲线用什么style
    markersize=15,  # Marker 的大小
)


ax2.set_frame_on(True)  # 可以让 legend永远在线的下面
plt.legend().set_visible(False) # 可以让 legend 消失， 但是仅仅针对最后一个子图
df2.plot(legend=None)  # 可以让所有子图的legend消失


# 几种创建 subplots的方法比较

# 1) 直接plot
plt.plot(....)  # 只画一张图时最方便

# 2) plt.subplots([row_n, col_n][, figsize=(width, height]))  (最终这个是最常用的)
# 以array的方式返回 fig 和 一组subplot的 axes
# 缺点是类似于 plt.legend 和 plt.xticks 这种方法只能作用于最后的一个ax
# 其实没有这个问题，可以直接通过ax画legened https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.legend.html
# TODO: 为什 g = sns.plot(ax=ax)中, 不能ax.legend(), 可以g.legend()


# 3) plt.subplot, 之后plt.xxx 一般就是等于 ax.xxx(也有小部分是找不到的)
# 似乎最好， 功能最全....


# 画完之后可以给该图组集中加一个title
plt.suptitle(name)

# Subplots篇 END -------------------------------------------------



# 非常有用的方法
plt.gca()  # get current axes




# jupyer内的奇技淫巧
# 可以直接隐藏代码
%%HTML
<script>
$('.input, .prompt, .output_stderr, .output_error, .output_result').hide();
</script>
# 记得留一个按钮回复代码
%%HTML
<button onclick="$('.input, .prompt, .output_stderr, .output_error, .output_result').toggle();">Toggle Code</button>
