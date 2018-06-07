#!/usr/bin/env python
# -*- coding:utf8 -*-



# Meta: 我在解决什么问题
# 加载和预处理数据变得代价较大，所以要用jupyter这种来。
# Jupyter调参比较困难，需要papermill来传参。
# 需要做的尝试比较多，需要一个多进程的框架来做尝试。
# 实验结果比较多，需要比较好地组织实验结果。
# 同时满足上述各种需求需要好的设计，我大概实现了这样一套设计。


# BEGIN config ---------------------------------------------------
# Stop to use sqlite to store the history
# Otherwise the multi-processes will conflicts.
# ~/.ipython/profile_default/ipython_config.py
c = get_config()
c.HistoryManager.enabled = False

# Configuring https://nbconvert.readthedocs.io/en/latest/config_options.html
# add below into  ~/.jupyter/jupyter_nbconvert_config.json
# "ExecutePreprocessor": {
#   "timeout": -1
# },

# Otherwise TimeoutError: Cell execution timed out



# TODO: some  error to be fixed

# I think here is the reason: https://stackoverflow.com/questions/24229953/exception-attributeerror-nonetype-object-has-no-attribute-remove?noredirect=1&lq=1
# Traceback (most recent call last):
#   File "/home/xiaoyang/anaconda2/lib/python2.7/threading.py", line 801, in __bootstrap_inner
#     self.run()
#   File "/home/xiaoyang/anaconda2/lib/python2.7/site-packages/ipykernel/parentpoller.py", line 36, in run
#     if os.getppid() == 1:
# AttributeError: 'NoneType' object has no attribute 'getppid'

# RuntimeError: Kernel died before replying to kernel_info

# It seems to consume a lot of time to save the file to disk

# FIXED
# Solution: https://github.com/tqdm/tqdm/issues/481
# Exception in thread Thread-7:
# Traceback (most recent call last):
#   File "/usr/lib/python3.6/threading.py", line 916, in _bootstrap_inner
#     self.run()
#   File "/home/vagrant/regex/lib/python3.6/site-packages/tqdm/_tqdm.py", line 144, in run
#     for instance in self.tqdm_cls._instances:
#   File "/usr/lib/python3.6/_weakrefset.py", line 60, in __iter__
#     for itemref in self.data:
# RuntimeError: Set changed size during iteration



# END   config ---------------------------------------------------





# BEGIN get_tasks ---------------------------------------------------
import os
import copy

# The parameters that will always included in the result path
# NOTE: So the default parameters should not change for compatibility of the code before
DEFAULT_PARAMETERS = {
}


def get_result_path(param, exp_path):
    '''
    这个函数的设计难点在于新加的参数要兼容前面的命名规则
    '''
    basename = ['SOMETHING_XXX']

    # 原本想法：
    # 尽量把可能考虑的因素在前面搞定
    # 没考虑到的因素加在后面兼容的部分
    # 现在想法：
    # 有了众多参数后，文件名实在是太长了，默认参数就不要显示了

    # BEGIN 向之前版本兼容的变量
    # # An example
    # # If not present, use the default value `mse` in ipynb.
    # if param.get('LOSS_FUNC_XXX', 'mse') != 'mse':
    #     basename.append('loss=%s' % param['LOSS_FUNC_XXX'])
    # END   向之前版本兼容的变量

    # This should be the last
    # This is for distinguishing different version of results for same parameters
    if "VERSION" in param:
        basename.append('v={}'.format(param["VERSION"]))
    return os.path.join(exp_path, '-'.join(basename))


def get_task_params(exp_path='exp_results'):
    parameters = []

    # for ....:
    #     parameters.append(param)
    # 尽量一组for循环搞定，新加的参数就直接往for循环里加层

    for param in parameters:
        p = copy.deepcopy(DEFAULT_PARAMETERS)
        p.update(param)
        param.update(p)

        # the res_path will be the place to save the result for the script
        res_path = get_result_path(param, exp_path)
        param['RES_PATH'] = res_path
    return parameters
# END   get_tasks ---------------------------------------------------


# BEGIN run_exp.py --------------------------------------------------
import os
import papermill as pm
from multiprocessing import Pool
import time
from get_tasks import get_task_params
import random
import shutil
from distutils.util import strtobool
import sys
from datetime import datetime

import argparse
import multiprocessing
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
        This script will run multiple experiments concurrently
''')
parser.add_argument('-c', dest='concurrency', type=int, help='Concurrency of tasks. How many tasks to   run concurrently', default=multiprocessing.cpu_count() * 3 // 4)
ARGS = parser.parse_args()


# 为了保证进度条不会出错
# TODO; to solve `RuntimeError: Set changed size during iteration`
from tqdm import tqdm
tqdm.monitor_interval = 0

DIRNAME = os.path.abspath(os.path.dirname(__file__))

RES_DIR = os.path.join(DIRNAME, 'exp_results/XXXX')
if not os.path.exists(RES_DIR):
    os.makedirs(RES_DIR)

import logging
logging.basicConfig(
        filename=os.path.join(RES_DIR, "task.log"),
        level=logging.INFO,
        format='%(asctime)s %(name)s (PID:%(process)d) [%(levelname)s]:%(message)s',  # name 是 logger的name
)
LOG = logging.getLogger(__file__)


def user_yes_no_query(question):
    from six.moves import input
    sys.stdout.write('%s [y/n]\n' % question)
    while True:
        try:
            return strtobool(input().lower())
        except ValueError:
            sys.stdout.write('Please respond with \'y\' or \'n\'.\n')


def task_wrapper(*args, **kwargs):
    ''' In case that some tasks are executed repeatedly'''
    start = datetime.now()
    fin_flag_path = os.path.join(os.path.dirname(kwargs['output']), 'fin_flag')
    if os.path.exists(fin_flag_path):
        print("Task has been finished before.")
    else:
        pm.execute_notebook(*args, **kwargs)
        open(fin_flag_path, 'a').close()# # touch to indicate the task has been finished
    return datetime.now() - start


def back_up_script():
    for fname in ['get_tasks.py', 'run_exp.py']:
        shutil.copy(os.path.join(DIRNAME, fname), RES_DIR)


if __name__ == '__main__':
    back_up_script()

    parameters = get_task_params(RES_DIR)
    if not user_yes_no_query("Total %d tasks. Concurrency=%d. Continue running?" %
                             (len(parameters), ARGS.concurrency)):
        sys.exit()

    # check "code_to_copy/backend/python_apps/processing_threading.py" for the latest version and detailed explaination
    # Command to kill all run_exp.py
    # ps aux | grep 'python run_exp.py' | grep -v grep  | awk '{print $2}' | xargs kill
    res = []
    tid = 0
    pool = Pool(ARGS.concurrency)

    random.shuffle(parameters)  # Useful when no enough time to run all exp.
    for param in parameters:
        res_path = param['RES_PATH']
        # This is folder is created for generating the script.
        if not os.path.exists(res_path):
            os.makedirs(res_path)
        kwargs = dict(
            notebook=os.path.join(DIRNAME, 'XXXXX.ipynb'),
            output=os.path.join(res_path, 'script.ipynb'),
            parameters=param)
        res.append((tid, kwargs, pool.apply_async(task_wrapper, [], kwargs)))
        tid += 1
        time.sleep(0.1)
    for i, args, r in res:
        try:
            print('task (%d / %d) ended, time:' % (i, tid), r.get())
            print('Args:\n', args)
        except Exception as e:
            LOG.exception(u"Type=%s, Args=%s.\nRun order=%d.\nTask args:\n%s" %
                          (type(e), e.args, i, str(args)))
    pool.close()  # TODO: If I put it before r.get(). The print info above will never output the data.
    pool.join()  # TODO: one must call close before call join
# END   run_exp.py --------------------------------------------------


# BEGIN exp_summary.ipynb --------------------------------------------------
# 汇总所有的实验结果
import os
import papermill as pm
import pandas as pd
from IPython.display import display
import numpy as np
RES_DIR = os.path.join('./exp_results/XXXX')
# get task from the valid
import imp
get_tasks = imp.load_source('get_tasks', os.path.join(RES_DIR, 'get_tasks.py'))

params_l = get_tasks.get_task_params(RES_DIR)
print(len(params_l))
data = {}

# get all keys
for params in params_l:
    for k in params:
        data[k] = []

for params in params_l:
    for k in data:
        data[k].append(params.get(k, np.nan))

sum_df = pd.DataFrame(data=data)


# get the parameters we've tuned except version
GB_ATTRS = []
for cname in sum_df:
    if len(sum_df[cname].astype(np.str).unique()) > 1 and \
				     cname not in ['VERSION', 'RES_PATH']:
        GB_ATTRS.append(cname)

for cname in GB_ATTRS:
    # convert to str for grouping.
    sum_df[cname] = sum_df[cname].astype(np.str)

sum_df['exp_n'] = sum_df.groupby(GB_ATTRS)['RES_PATH'].transform('count')


# XXX read the result from res_path
# read the pm data
for i, row in sum_df.iterrows():
    display(sum_df[i:i + 1])
    res_nb_path = os.path.join(row['RES_PATH'], 'script.ipynb')

    # READ  the config
    res_nb = pm.read_notebook(res_nb_path)
    res_nb.display_output('XXXX')

g_sum_df = sum_df.groupby(GB_ATTRS).mean()

# Check the affect of every parameters
for attr in GB_ATTRS:
    print(attr, '=' * 20)
    display(sum_df.groupby(attr).mean().loc[:, 'pretrain_group5_model_ar':'ft_group5_wr'])
    display(sum_df.groupby(attr).count().loc[:, 'pretrain_group5_model_ar':'ft_group5_wr'])

# END   exp_summary.py --------------------------------------------------


# BEGIN jupyter.ipynb -----------------------------------------------
# https://github.com/nteract/papermill
# 加 `parameters` tag
# 基本原理:
# - 参数：将相关cell的代码直接替换掉
# - 读取结果: 将结果存在output中， 但是隐藏不显示.  所以必须运行而且save之后才能被其他的脚本读取到
# TODO: 确认一下cwd 是哪里.  确定不会锁定为最终生成脚本的所在目录
# 传入list是可行的
# TODO: 确认一下传入字典是否可行

# 第一个cell放现在不需要调的参数 const
# 第二个cell放调参时的 default value.
# - 和get_task中的默认参数dict重复， 解决方法是只留一套，觉得再ipynb中留更省事(ipynb编程时方便)
# 第三个cell放 `parameters` tag,  表示只针对这次运行的参数
# 第四个cell放 Assertion，遇到不必要的参数组合直接退出  (和create tasks时的逻辑重复)
# 该代码时尽量保留原有功能，将其变成一个参数，这样方便调参， 也方便对比修改前后的区别。

# END   jupyter.ipynb -----------------------------------------------
