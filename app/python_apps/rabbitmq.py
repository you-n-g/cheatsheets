#!/usr/bin/env python
# coding:utf8


# 目录
# - 用户篇
# -


# ------------------------ 用户篇 ------------------------
# This adds a new user and password:
sudo rabbitmqctl add_user username password
# This makes the user a administrator:  可以通过 http://127.0.0.1:15672 管理队列
sudo rabbitmqctl set_user_tags username administrator
# This sets permissions for the user:  可以远程管理信息
sudo rabbitmqctl set_permissions -p / username ".*" ".*" ".*"


# list queues
# sudo rabbitmqctl list_queues




# pyrabbit
# https://pyrabbit.readthedocs.io/en/latest/
# pika 是通用的API， 有的rabbitmq的特有接口访问就不方便了
# 有各种各样的方式可参考 https://stackoverflow.com/a/27074594

