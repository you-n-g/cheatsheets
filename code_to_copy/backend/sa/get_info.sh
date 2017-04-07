#!/usr/bin/env bash


# kernal version
uname -a
cat /proc/version

# linux version
lsb_release -a
cat /etc/redhat-release  # 仅仅限于 redhat系列


# disk ，参考  backend/sa/disk.sh


# BEGIN 计算机性能状况

# 所有的 [参考](http://www.binarytides.com/collectl-monitor-system-resources-linux/)
collectl [-scd]

# 概念相关
# http://blog.sina.com.cn/s/blog_51d2a47a0101380o.html : 说明了vmstat, ps 和 top的CPU占用的关系
# vmstat 的100%-idle == ps的cpu占用/cpu核心数 == top的cpu占用/cpu核心数/物理cpu数目;
# 根据/proc/cpuinfo看概念： [源](http://www.cnblogs.com/emanlee/p/3587571.html)
# - 物理CPU数指装了几个CPU,即 "physical id"
# - cpu核心数指每个物理CPU的核心数量，即 "cpu cores"
# - 逻辑核数，即 "processor" 不同的数量, TODO : 因为超线程技术 区别于 物理CPU数 * CPU核心数????
# top的 CPU占用指 单位时间内 进程使用的CPU时间/单位时间 [来源](http://www.sosolinux.com/thread-463-1-1.html)
# troobleshooting
# iostat vmstat mpstat 第一次结果是 立马出来，这一般说明这个样本是从开机到现在的性能数据


# 查看进程的性能情况, 到文本。
COLUMNS=1024 top -bc -n1 -d 1
# COLUMNS=1024 设置屏幕宽度以防top按屏宽度自动truncate
# -b: batch mode
# -c: 显示 full command方便抓取
# -n1: 只迭代一次
# -d 1: 延迟1秒取样


# TODO
vmstat

# 针对到IO，精确的进程的
iotop

# htop: iotop top lsof的合体，  用户体验也非常好
lsof: 方向选中相关进程，l
iotop: TODO 看IO怎么实现

# perf TODO

# END   计算机性能状况



# BEGIN 查看进程相关
sudo lsof -i :XXX_PORT # 看XXX_PORT被哪个进程占用了
# END   查看进程相关




# 查看硬件信息
dmidecode
# dmidecode列出的信息常用的有
System Information -> Serial Number: GWPCZY1  # 查看序列号用于售后服务
Product Name: ThinkServer RD640  # 查看机器型号
Memory Device # 查看内存信息

# 查看网卡信息
lspci | grep Ethernet



# 查看进程信息
## 查看进程当前目录
pwdx pid # 其实是看   /proc/<pid>/pwd link到哪里
## 查看进程启动时间
ps -p PID -o lstart  



# 查看加载的内核模块
lsmod



# 查看running的程序的环境变量, 比如可以看到proxy到底有没有生效
xargs --null --max-args=1 < /proc/XXX_PID/environ



# 查看kernel模块的参数
systool -vm <Module name>
