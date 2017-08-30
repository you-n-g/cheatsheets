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
    fig, axes = plt.subplots(2, 2, figsize=(12,4)) # Unknown size unit.

    axes = axes.flatten() #  If we dont't flatten this, we have to use axes[0, 1] to select the table.

    axes[0].hist(n, bins=29)
    axes[0].set_title("Default histogram")
    axes[0].set_xlim((min(n), max(n)))
    axes[0].xaxis.set_label_text('Number of sectors with big loss in a day')
    axes[0].yaxis.set_label_text('Number of days with that number of sectors big loss')

    axes.axvline(x=np.median(n), color='g', label='median') # set label
    axes.axvline(x=np.mean(n), color='r', label='mean')

    axes[1].hist(n, cumulative=True, bins=29)
    axes[1].set_title("Cumulative detailed histogram")
    axes[1].set_xlim((min(n), max(n)));
    plt.legend() # show label
    plt.xticks(rotation=45)  # set a rotation for label
    plt.show()


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
    ax.plot(x,y, '-')
    # Set number of ticks for x-axis
    ax.set_xticks(x)
    # Set ticks labels for x-axis
    ax.set_xticklabels(x_ticks_labels, rotation='vertical', fontsize=18)
    plt.show()
