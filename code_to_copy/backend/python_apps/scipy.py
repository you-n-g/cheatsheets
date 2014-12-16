#!/usr/bin/env python
#-*- coding:utf8 -*-

''' TODO 理解这一段话
NumPy是一个定义了数值数组和矩阵类型和它们的基本运算的语言扩展。
SciPy是另一种使用NumPy来做高等数学、信号处理、优化、统计和许多其它科学任务的语言扩展。
Matplotlib是一个帮助绘图的语言扩展。
'''

# 我们来搞定科学计算

import numpy
from scipy import stats

XXX_ar = stats.pearsonr([XXX])
print stats.tvar(XXX_ar), stats.tstd(XXX_ar), stats.tmean(XXX_ar)

# pearson product moment efficent
print stats.pearsonr(XXX_LISTA, XXX_LISTB)


print numpy.log2(1024)
print numpy.log10(0)
print numpy.log(XXX)  #it's ln

print numpy.exp(1)

print numpy.e, numpy.pi





# 数学公式 # 不明白为什么叫special啊
import scipy.special as S
print S.log1p(1e-20)  ## 计算 ln(1 + 1e-20)




# 矩阵相关
# 我觉得这里有很多工具 http://blog.sina.com.cn/s/blog_70586e000100moen.html
x = numpy.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [1, 0, 1],
]).T  # 样本向量都按标准的列的形式给出

print numpy.cov(x, bias=1) # 如果需要除以 N 而不是 N-1， 则 bias=1

x = numpy.array([[2, 0], [0, 2]])
y = linalg.inv(x)  # 求逆矩阵
