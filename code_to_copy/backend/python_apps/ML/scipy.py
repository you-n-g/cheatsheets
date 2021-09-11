#!/usr/bin/env python
#-*- coding:utf8 -*-

# Outlines
# - pandas
#   - pandas cheatsheets
# - numpy
# - Interpretor/Jupyter


# 基本模板
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(color_codes=True)
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
from tqdm.auto import tqdm
# tqdm.pandas()  # for progress_apply
%matplotlib inline
%load_ext autoreload
# !less %

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


def softmax(x, axis=-1):
    """Compute softmax values for each sets of scores in x on axis `axis`."""
    e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e_x / e_x.sum(axis=axis, keepdims=True)



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


# 排序相关

from scipy.stats.mstats import rankdata
# rankdata  得到的rank是从1开始的，而且相同排名时会显示排名的平均
# 数值越大 rank值越大

np.argsort


# %% [markdown]
# # Outlines: pandas
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
pd.reset_index(drop=True, inplace=True)

# selecting is supported.  loc只支持label来 index, 如果想按下标顺序index， 必须用iloc
df.loc[BEGIN_ROW:END_ROW, BEGIN_COL:END_COL]  # such as df.loc[1:2, 'InnerCode':'IfWeekEnd']
# 分两种情况
# - 如果用loc[], 那么第一维肯定是行，第二维肯定是列.
# - 如果用loc, 那么只支持 第一维肯定是行，第二维肯定是列.

# 例子们
# 用 df.loc[A:B]和df[A:B] 是完全不一样的
# - loc会包含B，否则不包含B
# df[A] 和 df[A:B] 做的是完全不一样的事情！！ 前者是在列里面选，  后者是在行里面选
# df[A] 和 df.loc[A] 做的是完全不一会的事情！！！ 前者是在列里面选， 后者是在行里面选


for index, row in df.iterrows():
    print(row["c1"], row["c2"])
# 如果是想对index进行filter，直接对 df.index 进行计算转化为boolean index就行


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


# groupby会压缩数据，transform会变成长度相等的新的列。  http://pbpython.com/pandas_transform.html
df["total_price"] = df.groupby('order')["price"].transform('sum')


# 处理好 read_csv
## read_csv  load_csv 处理好多出来的索引列
df.to_csv("CSV_FILE")
df = pd.read_csv("CSV_FILE", index_col=0)
# OR
df.to_csv("CSV_FILE", index=False, header=False)
df = pd.read_csv("CSV_FILE")

## pandas 默认会把 na_values 中的所有字符串匹配的值都当成 NAN，如果想都把特殊列都当成字符串，不处理Nan，必须如下处理
df = pd.read_csv("CSV_FILE", keep_default_na=False, dtype={'word': np.str})


# get date number: make it easier to plot datetime
csv['trading_day'] = pd.to_datetime(csv['trading_day'])
csv['time_num'] = map(mdates.date2num, csv['trading_day'])  # TODO: will apply be faster????


# shift by group: https://stackoverflow.com/questions/26280345/pandas-shift-down-values-by-one-row-within-a-group
data.sort_values(['SecuAbbr', 'date'], inplace=True)
data['nextRisePct'] = data.groupby(['SecuAbbr'])['risePct'].shift(-1)


# 给group编号:
# https://stackoverflow.com/questions/41594703/pandas-assign-an-index-to-each-group-identified-by-groupby
df['idx'] = pd.Categorical(df['a'].astype(str) + df['b'].astype(str)).codes



# left join table:
all_data = pd.merge(key_score_loss_df, data.loc[:, ('date', 'SecuAbbr', 'nextRisePct')], how='left',
                    left_on = ['date', 'sec'], right_on = ['date', 'SecuAbbr'], suffixes=('', '_y'))  # suffix is necessary when
# 看看各种情况实际运作的例子: https://pandas.pydata.org/pandas-docs/stable/merging.html#brief-primer-on-merge-methods-relational-algebra
# NOTE: 如果合并之前有两列的名称一样，会自动改成 XXX_x, XXX_y, 下面的方法可以更好地处理这种情况
# https://stackoverflow.com/questions/19125091/pandas-merge-how-to-avoid-duplicating-columns



# equal to R table
df['col_name'].value_counts()
# sns.countplot  #我觉得这个可能是对应的图


# processing multi index
df = pd.read_csv(fname, encoding='gbk', names=['date', 'sector'], sep='\t', index_col=(0, 1))
df.index.get_level_values(0) # get the values of specific level
df.loc[<第一层索引的某个值>]  # 可以直接得到第一层索引特定值的dataframe, 并且去掉了第一层索引
df.loc[(<第一层索引的某个值>, <第二层索引的某个值>)]  # 如果只有两层索引， 那么就将得到一个row

df.loc(axis=0)[<第一层索引的slice>, <第二层索引的slice>]
# 会完全只看行index，slice相当于只对行的不同层级的索引过滤。
# 注意 df.loc(axis=0)[a, b] 和 df.loc(axis=0)[a, b:b] 没有区别。
# 最终得到的结果也不会去除索引
# NOTE: 如果希望用上面的方式slice， 需要先sort， 比如三层的。
# fac_hist_perf_df.sort_index(axis=1, level=[0, 1, 2], inplace=True)

# 最新发现这样会比较方便
df.loc[pd.IndexSlice[<第一层>, <第二层>], pd.IndexSlice[<第一层>, <第二层>]]


# 创建多级Index的column:
# https://datascience.stackexchange.com/a/9463
fac_hist_perf_df = pd.DataFrame(columns=pd.MultiIndex.from_tuples([(col, tp, wsz)
                                                                   for col in col_names
                                                                   for tp in ('return', 'normal_ic', 'rank_ic')
                                                                   for wsz in WINDOW_SZ]))
fac_hist_perf_df.sort_index(axis=1, level=[0, 1, 2], inplace=True)
# 不同级别的 dataframe merge 的时候可能会把多级 column 转化为单级的column。
# 所以想再加别的列的话， 直接赋值，通过相同的index来merge.
# 在pandas中的列赋值成series，相当于left join, left_index, right_index都True

# 也可以直接将nested dict 转化为 dataframe
pd.Dataframe({(outerKey, innerKey): values for outerKey, innerDict in dictionary.iteritems()
 for innerKey, values in innerDict.iteritems()})

# 如果想调整列的顺序，需要用reindex方法， 直接通过loc选似乎顺序不会变化。

# remove duplicated index
csv[~csv.index.duplicated(keep='first')]


# 如果希望drop掉一个层级的index，可以用这个  https://stackoverflow.com/a/22233719
df.columns = df.columns.droplevel()

# 向index添加一层索引
# https://stackoverflow.com/a/40225796
df.columns = pd.MultiIndex.from_product([df.columns, ['C']])



# Roling : https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.rolling.html
pd.Series(STH_LIKE_LIST).rolling(window=3, min_periods=1, center=True).mean()


# Filter data
# {'HIST_PERF_RANK_ADD': '10', 'HIST_PERF_TOP_RANK_N': '10', 'MAX_MS_MODEL_EPOCH': '120'}
df[(df[list(keys)] == pd.Series(keys)).all(axis=1)]


# 和mysql相连 有中文的情况
CONN = 'mysql://USERNAME:PASSWORD@IP:3306/fin_data?charset=utf8'
# 下面这种方式设置的 encoding不管用!!! 必须用上面的charset !!!!
# from sqlalchemy import create_engine; CONN = create_engine(DB_URI, encoding='utf8')
df = pd.read_sql(sql='select * from %s limit 10;' % table_name, con=CONN)
df.to_csv('%s.csv' % table_name, encoding='utf8')  # 这里的encoding必须设置，否则会报编码错误！！！！


# save to mysql
df.to_sql(con=CONN, name=table_name, if_exists='append', index=False)
# This will create table automatically


# datetime相关
# pandas 的 to_datetime 得到的对象不是 datetime,  和datetime比较时它必须放在左边
# pandas 的 datetime index也支持用 '2014-04-03' 这种str去索引和slice



# 各种形变  pivot, stack unstack
# http://nikgrozev.com/2015/07/01/reshaping-in-pandas-pivot-pivot-table-stack-and-unstack-explained-with-pictures/

# 本质是在 wide format(中间有多列是值) 和 long format(只有一列是值)之间转化

# pivot的motivation: 将表的内容变成index和column，方便选择
# pivot_table 的本质是选一列作为值， 其他的列作为行列的index和column
# 和pivot不同的地方
# - 可以指定多个列作为index或者column，达到multiple level的效果
# - 可以指定index的层级作为列： 可以直接指定index层级的名字， 或者传入一个array
# (比如index.get_level_values())
# 有点像先set_index(把表的内容放到index中)， 再unstack(把index中的内容放到column中)

# melt的motivation: 将index和column吸收到表的内容中
# 有一个表
# - 某几列是数据，表示varable， 列名是变量名
# - 其他的列是index, 用来定位一组数据
# - 需求是将表变为每一行一个值, 对于每个值, 每行有它的index和变量名
# 有点像先stack(把column堆叠到index中), 再reset_index(把index放到表内容中)

# 对于有多层级index的数据，互反的pivot_table和melt是这样的
# pivot_data = melt_data.pivot_table(index='date', columns='code', values='score')
# melt_data = pivot_data.reset_index().melt(id_vars=pivot_data.index.name).sort_index()


# 计算相关
pd.DataFrame({'B': [0, 1, 2, np.nan, 4]}).ewm()
# com, span, halflife, alpha都是用来定alpha的
# min_periods 表示最少前面有几个非NA才计算具体值
# adjust=True时(default), 使用这组权重计算平均: (1-alpha)**(n-1), (1-alpha)**(n-2), ..., 1-alpha, 1.
# adjust=False时， 值就直接这么计算: weighted_average[0] = arg[0]; weighted_average[i] = (1-alpha)*weighted_average[i-1] + alpha*arg[i].
# Ignore NA的情况我还不明白

# apply 和transform在groupby之后的区别
# - 假设他们会用f(x): .. return res 处理数据
# - 分组后得到的是一个子dataframe `sub_df`
# 设计motivation:
# - apply允许你对sub_df做任意处理，然后把group的key加成最外层的index 拼接所有数据
# - transform希望你将sub_df的每一列做完变换后原shape返回，最后得到的结果和原格式一样
#   - 比较适合做完变换之后和原值进行比较
# f输入输出的区别
# - 1) Input差别： apply中的x是sub_df，transform的x是sub_df每一个列(series)
# - 2) Output的差别: transform的返回值要么是scalar，否则会有长度限制，必须等于sub_df每一列的长度，apply没有这个限制
# - https://stackoverflow.com/questions/27517425/apply-vs-transform-on-a-group-object
# 其他
# - 当group axis=1时，行列关系就反过来了



# pandas性能问题
# fillna如果是一个常数，性能会非常好，如果是一个series, 性能会非常差!!!!!
# - 比如fillna mean，那么可以先减mean，再fillna(0)会极大地提升性能
#
# [  ] 我的猜想: 有时候loc不一定很慢, 可能是iloc调用时不会拷贝数据， loc调用时一定会拷贝数据
# - 需要高性能时尽量用df操作，避免底层拷贝(我感觉dataframe到np.array会自动拷贝数据，尽量让这种事情只发生一次)!!!


# pandas 的resample
# 个人理解:
# - 当rule是'M', 'A', 'Q'这种单个时期时，拿月做例子， resample的bin划分左右端是 上一个月的最后一天， 这一个月的最后一天；
# - closed=left  则每个区间包含 [上一个月的最后一天， 这一个月的最后一天)
# - closed=right 则每个区间包含 (上一个月的最后一天， 这一个月的最后一天]  (默认值)
# - 当rule是X个M时，我理解是从当前取整的时间开始的这个M的**闭区间**为分割点，之后每X个M再出现一个分割点。 所以第一个分割点就变成一个月了!!!
# 解决方法如下,   但是这个地方会有一个问题， 每六个月的最后一天被划分到下六个月了
df.resample('6M', closed='left')


## 一些要注意的点
# 在 slice 上的修改有时候会影响到 原数据的, 在 numpy 也是同样的,  numpy需要用  numpy.copy才能避免
# - 一般直接看是否有 SettingWithCopyWarning就行, http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
# - 会直接修改源数据的: a.loc[a[0] < 5, 'idx'] = False
# - 不会直接修改源数据的：a.loc[a[0] < 5]['idx'] = False
#   - 看样子是直接loc上赋值的才会修改源数据

# bool index 时，如果传入的是带有index的boolean值， 取值是看index + bool的结果
# - df[series或者bool index] 会从index中截取， df.loc[:, series]会从columns中获取数据
#
# NOTE, TODO: 从一列有indexing的值赋值给 另外一个indexing的值， 很可能赋值对应管是按indexing来的！！！  一一对应得转化为list
#
# 带index的 Series 之间加减法会按index对应值操作，而不是按位置顺序操作

# pandas 的index是基于 numpy array 而不是series.
# 所以使用的时候要注意不要想当然地用series支持的操作


# Dataframe之间的element-wize操作 基本都是按着
# index和col的索引对应的，最后的结果类似于outer join的形式.

# Pandas的很多操作默认是skipna=True的


## 理解文档中的一些词
# 对于一些聚合函数
# 1) axis for the function to be applied on:  代表每次应用这个函数时， 相当于将axis之外的维度固定住，变动这一个axis得到多个值进行聚合， 结果是axis被消除
# 2) count along a particular level, collapsing into a Series. :  代表按照level依次选取一批值，用函数聚合成一个值， 最后只剩这个level的一系列值。


# ## Outlines: pandas cheatsheets
# https://github.com/kailashahirwar/cheatsheets-ai

# pandas 相关  =========================================================================================



# TODO: preprocessing
from sklearn import preprocessing
# http://scikit-learn.org/stable/modules/preprocessing.html
min_max_scaler = preprocessing.MinMaxScaler()
min_max_scaler.fit(train_total_x)
train_resc_total_x = min_max_scaler.transform(train_total_x)
test_resc_total_x = min_max_scaler.transform(test_total_x)



# 验证结果相关
from sklearn.metrics import confusion_matrix, classification_report



# %% [markdown]
# # Outlines: numpy


# 坑!!!!!
# TODO: indexing, https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html
# Index 包括
# - Basic Slicing and Indexing: 当index是integer, slice和Ellipsis。 或者这些的组合的tuple
# - Advanced Indexing: non-tuple的sequance或者ndarray 或者是他们的tuple
#   - 如果都是ndarray:  result[i_1, ..., i_M] == x[ind_1[i_1, ..., i_M], ind_2[i_1, ..., i_M],
#                                                  ..., ind_N[i_1, ..., i_M]]
#       - 相当于会把index先都broadcast到统一维度和长度，然后从这几维选择
#   - Boolean array:  x[bool_obj] 完全相当于 x[bool_obj.nonzero()]
#       - 如果只有一个有个限制： 需要index的维度和被index的维度一致，没有broadcast
#       - 否则其他index混用时， 相当于 idx.nonzero()生成的几维替换成原来的一维。
# - 如果是basic slicing和 advanced indexing 的合并，我理解是先选出slicing，然后剩下的维度扩充成advanced indexing

# 问题  a[[1, 1]]:
# - 我理解空着都是全slicing，所以这一列是Advanced indexing.

np.eye(10)[1, 1]  # 取index是 1, 1的元素
np.eye(10)[[1, 1]] # 取第一行取两遍
np.eye(10)[(1, 1)] # 取index是 1, 1的元素

# slicing 会默认return views,  对views的直接修改会影响到元数据
# - 高级indexing 一直会返回返回copy
#  - b = a[<高级index>]; b += XXX; 不会对原ll 进行影响。
#  - 但是如果是 a[<高级index>] += XXX， 会对原来影响


# Broadcasting: https://docs.scipy.org/doc/numpy-1.13.0/reference/ufuncs.html#ufuncs-broadcasting
# 当多个array做element-wize function时，按下面的规则broadcasting
# - 对齐维度: 确定最大的dimension， 先prepend 长度为1的dimension来对齐所有dimension
# - 对齐维度长度： 所有维度要么长度相等，要么长度为1(相当于将1自动补齐成最大长度).
# 常见应用： 比如比较column和index的值时，可以(df.index.values.reshape(-1, 1) < df.column.values.reshape(1, -1))


# np.nan 的bug
# - bool(np.nan) is True
# - np.nan < > ==  等等都是 False;  所以依靠


# %% [markdown]
# # Outlines: Interpretor/Jupyter


# 存储整个环境变量
# https://stackoverflow.com/a/35296032
import dill # pip install dill
filename = 'globalsave.pkl'
dill.dump_session(filename)
# and to load the session again:
dill.load_session(filename)





# Jupyter/Ipython notebook 相关 BEGIN --------------------------
jupyter nbconvert --to=python [YOUR_NOTEBOOK].ipynb  # 会生成 [YOUR_NOTEBOOK].py 文件
jupyter nbconvert --to notebook --output OUT.ipynb --execute [YOUR_NOTEBOOK].ipynb # 如果没有指定 --to nbtebook，默认输出类型是html
# 不加output会生成 [YOUR_NOTEBOOK].html 或者 [YOUR_NOTEBOOK].nbconvert.ipynb

# Seems below method does not work
# Configuring https://nbconvert.readthedocs.io/en/latest/config_options.html
# add below into  ~/.jupyter/jupyter_nbconvert_config.json
"ExecutePreprocessor": {
  "timeout": -1
},
# Otherwise TimeoutError: Cell execution timed out

# 如果你想传参进去: 默认是无法直接传入参数到 sys.argv 中的



# 可以随意地display结果
from IPython.display import display
display(df)


# 将某个文件中的内容直接再当前的context下运行
# https://stackoverflow.com/a/42203142
# 这样可以方便项目管理
%run -i 'script.py'



# 处理文本数据可能会遇到的坑
# 文本最好开始就统一成utf8的
# - 不然之后计算长度容易出问题
# - 不然用文本做key后， 之后又改编码会导致之前代码出问题


# https://ipython.org/ipython-doc/3/config/extensions/autoreload.html
# Autoreload -> 方便直接  reload所有的Package
# %load_ext autoreload
# %autoreload
# 全都变成Autoreload也很爽!!!!!  直接看页面里面的aimport吧
# Pros
# - 相比于importlib有如下好处(文档写的是把最底层的class和functions直接做了替换)
#  - 已经在notebook初始化过的类, 不需要对import进来的类名重新赋值，
#  - importlib会有这种问题: insintance(老对象, 新类) 返回False
#  - aimport还可以直接自动每次加载最新的代码,  比较方便
# 其他
# - import时global的代码是不会再运行一遍的(因为不是函数对象)
# - 在module里面新定义函数居然是可以的!!! 但是删除之后会把引用指向一个不可调用的 _io.TextIOWrapper
# 对编程方式的里程碑的革新
# - 解决了这个gap: 你coding可以只关注一小块，每次验证的时候却需要跑全部代码
# - 之前的方法: 也可以保存状态， 但是加载新代码极其麻烦，而且为了能方便加载，代码结构会被弄得非常混乱
# DEBUG:
# - 如果发现无法加载新代码， 可能是因为下面的原因
#    - 新代码的.py文件中有语法错误
#    - 是改完新新新代码后才 `%autoreload 1`(看完文档后觉得不应该这样，但是实际感觉文档编辑操作总是能触发一些东西)
# 坑
# - 有可能会造成 改变了方法的类和父类之间失去了继承关系, isinstance出错, 子类中调用super()出错 (重启一下kernel就好了)
#   - 在父类和子类在同一个 .py 文件中时，曾经稳定多次复现



# 可以用vim写代码送到 jupyter notebook kernel
%connect_info  # 利用这里得到的结果，可以用 `jupyter console` 直接和相应的kernel链接

# 路线1) 直接写 py代码，  最后转成noteobok
# 写完的使用jupyter  notebook的代码存在.py文件后， 可以直接用jupyter run XXX 运行
# 最后如果硬要转化成ipynb
# - 可以通过ipynb-py-convert, 写的时候多注意用 # %%
# - 也可以用python2jupyter

# 路线2) jupyter notebook开启后， 用 qtconsole 看结果， 用vim + jupytext辅助 编辑文件， 用 "jupyter-vim/jupyter-vim" 发送结果
# - jupyter notebook 尽量直接打开 `.py` 文件， 这样各方操作比较一致

# 路线3) 同上， 不同的是 直接用 vim-slime 发送&看结果， embed解决无法识别 %cpaste 的问题
# - 这个的优点是可以不用在电脑上预装
# - conda install -c conda-forge jupyter_console


# 有用的magic fucntions:
# 可以把文件输入都放到ipynb中  %notebook out.ipynb



# Jupyter/Ipython notebook 相关 END   --------------------------
