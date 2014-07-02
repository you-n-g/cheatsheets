#!/usr/bin/env bash


# kernal version
uname -a
cat /proc/version

# linux version
lsb_release -a



# disk ，参考  backend/sa/disk.sh


# BEGIN 计算机性能状况

# 所有的
collectl [-scdu]

# TODO
vmstat

# 针对到IO，精确的进程的
iotop

# htop: iotop top lsof的合体，  用户体验也非常好
lsof: 方向选中相关进程，l
iotop

# END   计算机性能状况




# 查看硬件信息
dmidecode
# 常用的有
System Information -> Serial Number: GWPCZY1



# 查看进程当前目录
pwdx pid # 其实是看   /proc/<pid>/pwd link到哪里



# 查看加载的内核模块
lsmod



