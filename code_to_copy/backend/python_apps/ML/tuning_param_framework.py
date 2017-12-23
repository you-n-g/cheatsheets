#!/usr/bin/env python
#-*- coding:utf8 -*-


# backend/python_apps/ML/scipy.py



# BEGIN get_tasks ---------------------------------------------------
import os
import copy
import numpy as np

DEFAULT_PARAMETERS = {
}

def get_result_path(param, exp_path):
    basename = 'SOMETHING_XXX'

    # This is for distinguishing different version of results for same parameters
    if "VERSION" in param:
        basename += '-%s' % param["VERSION"]
    return os.path.join(exp_path, basename)

def get_task_params(exp_path='exp_results'):
    parameters = []

    # for ....:
    #     parameters.append(param)

    for param in parameters:
        p = copy.deepcopy(DEFAULT_PARAMETERS)
        p.update(param)
        param.update(p)

        # the res_path will be the place to save the result for the script
        res_path = get_result_path(param, exp_path)
        param['RES_PATH'] = res_path
        # This is folder is created for generating the script.
        if not os.path.exists(res_path):
            os.makedirs(res_path)
    return parameters
# END   get_tasks ---------------------------------------------------


# BEGIN run_exp.py --------------------------------------------------
import os
import papermill as pm
import copy
from multiprocessing import Pool
import numpy as np
import time
from get_tasks import get_task_params
import random

DIRNAME = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    pool = Pool(5)
    res = []
    tid = 0
    exp_path = os.path.join(DIRNAME, 'exp_results')
    parameters = get_task_params(exp_path)
    random.shuffle(parameters)  # Useful when no enough time to run all exp.
    for param in parameters:
        kwargs = dict(
            notebook=os.path.join(DIRNAME, 'XXXXX.ipynb'),
            output=os.path.join(param['RES_PATH'], 'script.ipynb'),
            parameters=param)
        res.append((tid, pool.apply_async(pm.execute_notebook, [], kwargs)))
        tid += 1
        time.sleep(0.2)
    for i, r in res:
        try:
            print 'task (%d / %d) ended: ' % (i, tid), r.get()
        except Exception, e:
            print u"Type=%s, Args=%s" % (type(e), e.args)
    # pool.close() # TODO: If I put it before r.get(). The print info above will never output the data.
    # pool.join() # TODO: one must call close before call join
# END   run_exp.py --------------------------------------------------


# BEGIN exp_summary.py --------------------------------------------------
# 汇总所有的实验结果
import os
import papermill as pm
from get_tasks import get_task_params, get_result_path
import pandas as pd
from IPython.display import display

sum_pd = {}
for param in get_task_params():
    for k, v in param.items():
        if k not in sum_pd:
            sum_pd[k] = []
        sum_pd[k].append(v)
sum_pd = pd.DataFrame(sum_pd)


for i, row in sum_pd.iterrows():
    display(sum_pd[i:i + 1])
    res_nb_path = os.path.join(row['RES_PATH'], 'script.ipynb')

    # READ  the config
    res_nb = pm.read_notebook(res_nb_path)
    res_nb.display_output('XXXX')

# END   exp_summary.py --------------------------------------------------


# BEGIN jupyter.ipynb -----------------------------------------------
# https://github.com/nteract/papermill
# 加 `parameters` tag
# 基本原理:
# - 参数：将相关cell的代码直接替换掉
# - 读取结果: 将结果存在output中， 但是隐藏不显示.  所以必须运行而且save之后才能被其他的脚本读取到
# TODO: 确认一下cwd 是哪里
# TODO: 确认一下传入字典是否可行

# 第一个cell放现在不需要调的参数
# 第二个cell放正在调的参数
# 该代码时尽量保留原有功能，将其变成一个参数，这样方便调参， 也方便对比修改前后的区别。

# END   jupyter.ipynb -----------------------------------------------
