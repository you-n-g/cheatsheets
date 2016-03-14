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
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

DATETIME=`date +%Y-%m-%d:%H:%M:%S`



# .bashrc
export EDITOR=`which vim`


# bash 的一些工具
# 多线程
for i in `seq 1 5`; do
{
    #commands
    sleep 1
    echo done
}&
done
wait
echo "all done"


# 同时打开多个窗口
xfce4-terminal/gnome-terminal --working-directory="/home/young/" \
    --tab --title CB02  -e 'bash -c "ls / ; exec bash"' \
    --tab --title CB02  -e 'bash -c "ls ~ ;" '


# 用分隔符处理数组
while IFS=';' read -ra XXX_ARR; do
    # 对$IN中的每一行分割成数组
    # 如果只要处理一行，就直接用： IFS=';' read -ra XXX_ARR <<< "$IN"
    for i in "${XXX_ARR[@]}"; do
        # "$@" 两要素保证了分割后某个元素有空格也会被当成一个元素处理！！！！
        # process "$i"
    done
done <<< "$IN"




# 管理服务
service --status-all  # 查看所有服务的状态




# 修改hostname
# 先改 /etc/hosts  /etc/hostname， 然后
hostname -F /etc/hostname



# ubuntu server 中文乱码问题, 照着 http://www.cnblogs.com/top5/archive/2011/02/23/1962390.html 的前半部分做


# 类似于git 的格式查看两个文件夹下的代码区别
diff -bur folder1/ folder2/


# 写脚本
test "$XXX_STRING" = "XXX_STR" && echo True
