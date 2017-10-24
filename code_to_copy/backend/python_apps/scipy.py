#!/usr/bin/env python
#-*- coding:utf8 -*-

''' TODO 理解这一段话
NumPy是一个定义了数值数组和矩阵类型和它们的基本运算的语言扩展。
SciPy是另一种使用NumPy来做高等数学、信号处理、优化、统计和许多其它科学任务的语言扩展。
Matplotlib是一个帮助绘图的语言扩展。
'''

# 我们来搞定科学计算

import numpy as np
from scipy import stats

XXX_ar = stats.pearsonr([XXX])
print stats.tvar(XXX_ar), stats.tstd(XXX_ar), stats.tmean(XXX_ar)

# pearson product moment efficent
print stats.pearsonr(XXX_LISTA, XXX_LISTB)


print np.log2(1024)
print np.log10(0)
print np.log(XXX)  #it's ln

print np.exp(1)

print np.e, np.pi





# 数学公式 # 不明白为什么叫special啊
import scipy.special as S
print S.log1p(1e-20)  ## 计算 ln(1 + 1e-20)




# 矩阵相关
# 我觉得这里有很多工具 http://blog.sina.com.cn/s/blog_70586e000100moen.html
x = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [1, 0, 1],
]).T  # 样本向量都按标准的列的形式给出

print np.cov(x, bias=1) # 如果需要除以 N 而不是 N-1， 则 bias=1

x = np.array([[2, 0], [0, 2]])
y = linalg.inv(x)  # 求逆矩阵


# 大概瞧一瞧数据长啥样
from scipy import stats
print stats.describe(data.astype(np.float).flatten())


# 存取数据要注意的问题
# 数据都会被转化为 array，如果是list大概感觉不到太大区别，如果是dict则需要调用下面的方法
np.load('dict_data.npy').item()




# 数据选择相关
a = np.array(range(10))
a[np.logical_and(3 < a, a < 8)] # 因为 a < 3 会返回是否满足要求的 boolean 矩阵， 这个矩阵作为选择， 最终得到筛选之后的数据。
# 但是array之间无法直接运行 and 或者 or 运算， 


# pandas 相关  =========================================================================================
# pandas中，一张表是 pandas.core.frame.DataFrame, 一行或一列数据是pandas.core.series.Series
# 用pandas可以让数据本身包含很多信息，不用单独再对行列再进行描述
import pandas as pd
import os

csv_list = []
for fname in os.listdir(STOCK_PRICE_PATH):
    if fname.endswith('.csv'):
        fpath = os.path.join(STOCK_PRICE_PATH, fname)
        csv_list.append(pd.read_csv(fpath, encoding='utf8')) # 事后去逐行encoding会非常非常慢. 不加encoding，得到的str列都是str，而不是utf8
df = pd.concat(csv_list)

# selecting is supported.  loc只支持label来 index, 如果想按下标顺序index， 必须用iloc
df.loc[BEGIN_ROW:END_ROW, BEGIN_COL:END_COL]  # such as df.loc[1:2, 'InnerCode':'IfWeekEnd']
# 用 df.loc[A:B]和df[A:B] 是完全不一样的
# - loc会包含B，否则不包含B
# df[A] 和 df[A:B] 做的是完全不一样的事情！！ 前者是在列里面选，  后者是在行里面选
# df[A] 和 df.loc[A] 做的是完全不一会的事情！！！ 前者是在列里面选， 后者是在行里面选

for index, row in df.iterrows():
    print row["c1"], row["c2"]


# 如何操作Groupby的数据: groupby后会出现多重索引
grouped_top_data = df.groupby('date')['score'].nlargest(N_LARGEST) # This will return a pandas.core.series.Series
# If you want to get index by group
for groupby_name, group in grouped_top_data.groupby(level=0):
    gidx = []
    for midx, score in group.iteritems():
        date, idx = midx
        gidx.append(idx)
    # the ineex in the group will be in gidx now
# If you want to get index directly
for midx, score in grouped_top_data.iteritems():
    date, idx = midx
    


# read_csv  load_csv 处理好多出来的索引列
df.to_csv("CSV_FILE")
df = pd.read_csv("CSV_FILE", index_col=0)
# OR
df.to_csv("CSV_FILE", index=False)
df = pd.read_csv("CSV_FILE")


# shift by group: https://stackoverflow.com/questions/26280345/pandas-shift-down-values-by-one-row-within-a-group
data.sort_values(['SecuAbbr', 'date'], inplace=True)
data['nextRisePct'] = data.groupby(['SecuAbbr'])['risePct'].shift(1)



# left join table
all_data = pd.merge(key_score_loss_df, data.loc[:, ('date', 'SecuAbbr', 'nextRisePct')], how='left', left_on = ['date', 'sec'], right_on = ['date', 'SecuAbbr'])




# equal to R table
df['col_name'].value_counts() 


## 一些要注意的点
# 在 slice 上的修改有时候会影响到 原数据的, 在 numpy 也是同样的,  numpy需要用  numpy.copy才能避免
# - 一般直接看是否有 SettingWithCopyWarning就行, http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
# - 会直接修改源数据的: a.loc[a[0] < 5, 'idx'] = False
# - 不会直接修改源数据的：a.loc[a[0] < 5]['idx'] = False
# bool index 时，如果传入的是带有index的boolean值， 取值是看 index + bool的结果， 而不是

# pandas 相关  =========================================================================================



# 验证结果相关
from sklearn.metrics import confusion_matrix, classification_report
