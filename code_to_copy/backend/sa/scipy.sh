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



