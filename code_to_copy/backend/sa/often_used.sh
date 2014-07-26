#!/bin/bash


# 测试邮件连通性
echo "XXX" | mail -a "From: XXX@XXX.XXX" -s "XXX" 


# BEGIN 远程挂载 VVVVVVVVVVVVVVVVVVVVV
apt-get install sshfs
sshfs root@opvm:/ /mnt/opvm/
umount /mnt/opvm/
# 如果默认指定key挂载(如用root操作)
# Host *
#     IdentityFile /home/young/.ssh/id_rsa
#     User username



# END   远程挂载 ^^^^^^^^^^^^^^^^^^^^^



# 挂载内存当文件系统使用
mount -t tmpfs -o size=1024m tmpfs /mnt/ram




# 一些常常需要的变量
set -x # 设置允许的时候会把命令写出来， 而且会在命令前面输出+
PROJECT_PATH=`dirname "$0"`
PROJECT_PATH=`cd "$PROJECT_PATH"; pwd`

