#!/usr/bin/env python
#-*- coding:utf8 -*-

# interactive: https://blog.dominodatalab.com/interactive-dashboards-in-jupyter/
# you must install this extension https://github.com/jupyter-widgets/ipywidgets
# 可能会遇到这个错误  Widget Javascript not detected.  It may not be installed or enabled properly
# 最终没有解决


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

    x = np.linspace(0.0001, 1, 100)
    right_axes = axes.twinx()
    for tickset in [axes.xaxis.get_major_ticks(), axes.yaxis.get_major_ticks(),
		    right_axes.xaxis.get_major_ticks(), right_axes.yaxis.get_major_ticks()]:
	for tick in tickset:
	    tick.label.set_fontsize(fontsz)
    axes.plot(x, np.exp(x), ls='b--',label='exp')
    right_axes.plot(x, np.log(x), ls='r+', label='log')
    h1, l1 = axes.get_legend_handles_labels()
    h2, l2 = right_axes.get_legend_handles_labels()

    axes.set_xlabel("X", fontsize=fontsz)
    axes.set_ylabel("Y", fontsize=fontsz)
    right_axes.set_ylabel("YY", fontsize=fontsz)
    plt.legend(h1+h2, l1+l2, fontsize=fontsz)
    plt.xticks(rotation=45)
    plt.yticks(fontsize=fontsz)  # this will decide the right axes
    plt.show()


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

# color是一个字符串表示的 (n,) 的 dataframe, 它有自己的index
fd_len = filtered_dataframe.shape[0]
str_colors = ["#%02x%02x%02x" % tuple((np.array(color) * 255).astype(np.int)) for color in sns.color_palette("Blues", fd_len)]
# row_colors 是一个data frame
row_colors=pd.DataFrame(data=str_colors, index=filtered_dataframe.index)
# {row,col}_cluster: 设置是否要对行或者列做cluster
g = sns.clustermap(filtered_dataframe, row_cluster=False, row_colors=row_colors, figsize=(24, 24))
## 返回值是:  A ClusterGrid instance.
plt.show()



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

    # share x and y
    ax2 = plt.subplot(2, 1, 2, sharex=ax1, sharey=ax1)
    ax2.scatter(t, s3)

    plt.show()


