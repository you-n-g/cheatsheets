#!/bin/sh


# 目录
# - 基本概念

# ref
# https://conda.io/docs/user-guide/tasks/manage-python.html
# conda特别慢，它到底在干什么。
# https://www.anaconda.com/understanding-and-improving-condas-performance/
# conda比较慢的地方在于它需要根据你当前的环境解析 装什么样的包和依赖能满足你当前的需求; pip就直接安装你当前的包和依赖，不管你当前系统的状态
# 把所有相关的包的约束汇总起来是一个NP问题


# # Outlines: conda相关

# search
conda search --full-name python


# create a new environment
conda create -y -n py3 python=3 anaconda
# 其中anaconda是为了把科学计算相关的东西都装上, 加上它会导致安装大量的包，最终导致环境巨慢。


# show installed envs
conda info --envs


# active
source activate py36


# deactive
source deactivate


# set default environment: https://stackoverflow.com/questions/28436769/how-to-change-default-anaconda-python-environment
# Add some command to conda


# save the configuration of environment
# https://conda.io/docs/user-guide/tasks/manage-environments.html#building-identical-conda-environments
# 下面的好像有点问题， papermil 似乎没有安装好
# conda list --explicit > spec-file.txt
# conda create --name <YOUR ENV> --file spec-file.txt

conda env export --name base > environment.yml
conda env create -f environment.yml  # create an environment
conda env update -f environment.yml  # update current envrionment
# conda 无法复制环境，只能通过这种折中的方式达到复制的目的 conda remove --name old_name --all
conda create --name new_name --clone old_name
conda remove --name old_name --all


# 有时候 conda的包依赖于 .so文件，现在找.so文件似乎有bug
# https://stackoverflow.com/a/46833531


# # Outlines: pip相关
# 换成国内的源: https://mirrors.tuna.tsinghua.edu.cn/help/pypi/
