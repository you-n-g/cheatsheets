#!/bin/sh

# ref
# https://conda.io/docs/user-guide/tasks/manage-python.html

# search
conda search --full-name python


# create a new environment
conda create -n py36 python=3.6 anaconda


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

conda env export > environment.yml
conda env create -f environment.yml  # create an environment
conda env update -f environment.yml  # update current envrionment



# 有时候 conda的包依赖于 .so文件，现在找.so文件似乎有bug
# https://stackoverflow.com/a/46833531
