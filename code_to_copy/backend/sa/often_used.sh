#!/bin/bash

# # Outlines:
# - 


# Cheatsheet catalog
# - 语法篇
# - find篇


# 其他cheatsheet
# https://github.com/skywind3000/awesome-cheatsheets/blob/master/languages/bash.sh


# 测试邮件连通性
echo "content" | mail -a "From: XXX@XXX.XXX" -s "<subject>"  <mail_address>
# sudo apt-get install mailutils



# BEGIN 远程挂载 VVVVVVVVVVVVVVVVVVVVV
apt-get install sshfs
sshfs root@opvm:/ /mnt/opvm/
umount /mnt/opvm/
# 如果默认指定key挂载(如用root操作)
# Host *
#     IdentityFile /home/young/.ssh/id_rsa
#     User username



# END   远程挂载 ^^^^^^^^^^^^^^^^^^^^^



# 用户权限管理 VVVVVVVVVVVVVVVVVVV
sudo useradd -m -s /bin/bash -G NEW_USER NEW_USER
# -m 表示创建用户的时候创建主目录
# 修改用户的某一特性时使用 usermod，这时之前的权限无法生效，这时可以用下面两个命令之一来切换到新的权限
su - $USER
newgrp <NEW_GROUP>

# 如果修改了用户的组，是无法立即生效的。


# 针对某个组或者用户设置权限
# https://askubuntu.com/a/609201
# 各种 *acl 命令

# 用户权限管理 ^^^^^^^^^^^^^^^^^^^


# 挂载内存当文件系统使用
mount -t tmpfs -o size=1024m tmpfs /mnt/ram




# 一些常常需要的变量
set -x # 设置允许的时候会把命令写出来， 而且会在命令前面输出+

## = must used instead of ==
# 第一行是为了防止代码直接被贴到 console里面跑的情况; else里面的数值既可以处理跑脚本的情况，也可以处理source的情况
# 如果想区分 source 和 跑脚本的情况， 请参考下面
# https://unix.stackexchange.com/questions/4650/determining-path-to-sourced-shell-script
if [ $0 = "-bash" ]; then
    DIR=`pwd`
else
    DIR="$( cd "$(dirname $(readlink -f "$0"))" ; pwd -P )"
fi

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

# 这个工具似乎更好用，还可以控制线程池，相当于每一行一个命令:  apt-get install parallel
# 写法1
seq 1000 | parallel -j 8 --workdir $PWD ./myrun {} # https://stackoverflow.com/questions/5547787/running-shell-script-in-parallel

# 写法2
for year in `seq 10`
do
    echo "COMMAND $year"
done | parallel -j 8 --workdir $PWD


# 等待另外一个进程
# https://unix.stackexchange.com/questions/427115/listen-for-exit-of-process-given-pid
timeout $timeout tail --pid=$pid -f /dev/null


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
# 方法 1)
# 先改 /etc/hosts  /etc/hostname， 然后
hostname -F /etc/hostname
# 方法 2)
hostnamectl set-hostname HOSTNAME
# 然后重新登录




# ubuntu server 中文乱码问题, 照着 http://www.cnblogs.com/top5/archive/2011/02/23/1962390.html 的前半部分做


# 类似于git 的格式查看两个文件夹下的代码区别
diff -bur folder1/ folder2/


# 写脚本
test "$XXX_STRING" = "XXX_STR" && echo True




# Cent OS / Red Hat 系列常常会用到的

## selinux 篇
sestatus  # 查看selinux的状态
vim /etc/selinux/config  # 设置disabled

iptables 和 selinux 并不是同时开关，关了selinux后还得再关iptables


## 服务管理篇
chkconfig --list  # 列出来有什么服务
chkconfig XXX on  # 开启开机启动

## 网络配置篇 见interfaces


# Debian系列常用的

## 关闭防火墙
service ufw stop; ufw disable  # 其实从来没有确认过这个会不会影响





# 基本语法篇/常识

if ! grep "^proxy_up" ~/.bashrc ; then
elif
else
fi

if [ ! $? -eq 0 ]; then
# 参见 ./WritingShellScripts.wiki
#  -e file  # 文件是否存在


cmd >> all.log 2>&1  # cmd &>> all.log 这个命令效果相同， 但是低版本的bash可能不支持; 2>&1 表示将 Red. STDERR to "where stdout goes" Note that the interpretion "redirect STDERR to STDOUT" is wrong.
cmd &> all.log
cmd > stdout.log 2>stderror.log

# sudo 保持环境变量
sudo -E # 这个能保持绝大部分环境变量
sudo env "PATH=$PATH" godi_console  # 因为 secure_path 的配置，所以path无法用-E直接保存

# 切换到用户执行command最好用 -l，不然不会执行 .bashrc中的信息
# https://unix.stackexchange.com/a/29811
su -l $USER -c "COMMAND" -s /bin/bash
# 另外一个坑就是 $USER 的默认shell不是bash， 所以并不会设置bash的环境变量

# 为什么.bashrc用的多: ~/.profile 一般会读 ~/.bashrc,  所以如果你用bash, 只要是 login shell 或者 interactive shell, ~/.bashrc是就可以被读到.
# https://stackoverflow.com/a/415444


# 第二套理解
# http://feihu.me/blog/2014/env-problem-when-ssh-executing-command-on-remote/
|------------------+-------+-------------+-----------------|
|                  | login | interactive | non-interactive |
|                  |       | non-login   | non-login       |
|------------------+-------+-------------+-----------------|
| /etc/profile     | A     |             |                 |
|------------------+-------+-------------+-----------------|
| /etc/bash.bashrc |       | A           |                 |
|------------------+-------+-------------+-----------------|
| ~/.bashrc        |       | B           |                 |
|------------------+-------+-------------+-----------------|
| ~/.bash_profile  | B1    |             |                 |
|------------------+-------+-------------+-----------------|
| ~/.bash_login    | B2    |             |                 |
|------------------+-------+-------------+-----------------|
| ~/.profile       | B3    |             |                 |
|------------------+-------+-------------+-----------------|
| BASH_ENV         |       |             | A               |
|------------------+-------+-------------+-----------------|


| Mode                          | 设计目的             | 涉及配置文件系列 | 如何识别                                                  |
|-------------------------------+----------------------+------------------+-----------------------------------------------------------|
| login shell & non-login shell | 针对登录用户做设置   | profile 系列配置 | echo $0 : "-bash" 是login shell, "bash" 是non-login shell |
| Interactive & non-interactive | 针对交互式用户做设置 | rc系列配置       | echo $PS1 : 设置了这个变量是login shell                   | 
- 第一层:适用于所有shell
- 第二层:用户有不同的shell，run commands

# 环境变量找不到的解决方案: 实现一个启动脚本, 头部的位置写 #!/bin/bash --login



# shell函数取参数
# http://stackoverflow.com/questions/12314451/accessing-bash-command-line-args-vs
# for 循环时会有大量的不同
# $* 和 $@ 会把你引号包住的全拆开
# "$*" 会把各个段都合并成一个
# "$@" 常常是我们想要的， 引号包住的在一起， 该分开的分开
# 有引号空格数量也不一致时， echo $word 和  echo "$word" 是有区别的


# read the configure
MINIBATCH_SIZE=64
NUMBER_OF_MINIBATCHES=100

for i in "$@"
do
case $i in
    -m=*|--mini_batch_size=*)
    MINIBATCH_SIZE="${i#*=}"
    shift # past argument=value
    ;;
    -n=*|--num_batch=*)
    NUMBER_OF_MINIBATCHES="${i#*=}"
    shift # past argument=value
    ;;
    --default)
    DEFAULT=YES
    shift # past argument with no value
    ;;
    *)
            # unknown option
    ;;
esac
done
echo "Mini Batch Size  = ${MINIBATCH_SIZE}"
echo "Number of Batch = ${NUMBER_OF_MINIBATCHES}"


# read args with default value
# https://stackoverflow.com/questions/9332802/how-to-write-a-bash-script-that-takes-optional-input-arguments
ARG1=${1:-DEFAULT_ARG1}


# for pairs array
# https://stackoverflow.com/questions/14370133/is-there-a-way-to-create-key-value-pairs-in-bash-script
for i in a,b c_s,d ; do
  KEY=${i%,*};
  VAL=${i#*,};
  echo $KEY" XX "$VAL;
done
# 看不懂的操作看 http://tldp.org/LDP/abs/html/parameter-substitution.html



# 进程替换 / Process substitution:  相当于把里面这组命令的输出或者输入 替换成一个文件；方便有些命令不接受stdin，只能接受文件名做参数。
diff <(sort file1) <(sort file2) # >(command)  <(command)




# 数值计算
for ((train=2006, test=2012; test < 2017; train++, test++ )) ; do
    train_s=${train}0101
    train_e=$((test - 1))1231
done


# 一般shell软件分 带-的参数，  和不带-的参数。  为了消除歧义，一般 -- 代表带-的参数的结束


# 用户相关
adduser xiaoyang
usermod -aG sudo xiaoyang



# crontab

# debug crontabs
# https://stackoverflow.com/questions/4883069/debugging-crontab-jobs
# 1) add log
# 2) debug:  >> /tmp/log.crontab  2>&1





# Supervisor
supervisorctl  # 执行命令后输入 help 可以看到相应的可用的服务
sudo  supervisorctl status # 可用的服务
# 写完服务之后一定要记得
sudo  supervisorctl update

# 一个典型的服务如下所示, 只用关心启动的命令.
# https://serversforhackers.com/c/monitoring-processes-with-supervisord
[program:crawler]
command=/home/xiaoyang/anaconda3/bin/python main.py --config crawler.yml
directory=/home/xiaoyang/repos/movingb
autostart=true
autorestart=true
user=xiaoyang
environment=PATH="/home/xiaoyang/anaconda3/bin/:%(ENV_PATH)s"  # Path 必须这样设定
stopasgroup=true  # Supervisor 在关闭进程的时候只会关闭command的进程， 不会关闭子进程。 这样可以在执行stop命令时把所有整个组的进程都关闭掉
# 之前按我的经验，如果把 command变成了一个shell，它不会去对shell启动的子进程发送kill命令



# 设置用户权限
for p in $FIELS
do
    sudo setfacl -m g:limit_group:000  $p
done
sudo usermod -aG limit_group $AIAS






# Tricks BEGIN  ------------------------------------

# sudo 和 su 保留用户的环境变量: 
sudo -i -u xiaoyang sh -c 'echo "$PATH"'
sudo su - xiaoyang sh -c 'echo "$PATH"'

# bash读入stdin作为运行脚本，同时还加上参数; - 或者 -- 代表bash这个命令已经处理完所有的bash options，后面可以接filename和arguments了
echo 'echo $@' | bash -s - -lst

# Tricks END    ------------------------------------







# 语法篇BEGIN --------------------------------------

# EOF的用法
# https://stackoverflow.com/a/30728472
# 有双引号时(如"EOF"), 里面的内容一定不转义

# 符号的解释
## 单分号
## - 一般是用来分割代码块(解决一行要执行多个命令的问题)，常常可以被回车代替; 
## - 分号前面不需要空格分隔
## 双分号
## - 终止case项
## 冒号
## - 等价于 NOP/true/什么都不干但是返回true,
## - `while :` 等于不断循环
## - `then :` 代表这支什么都不干
## 单中括号[ ]是 shell中的语法糖， 相当于单句的test
## - 中括号的内部需要空格分隔
## Ref
## - https://cnbin.github.io/blog/2015/06/28/bash-zhong-de-te-shu-fu-hao-1/

## if 从句中， 不同的命令可以用  ！ -a -o  之类的逻辑运算符连接
## - [  ] 本质是test，也算命令的一种， 可以和其他命令用逻辑运算链接


# 把带空格的 ARGUMENTS 当成多个分开的arguments
eval $ARGUMENTS

# 语法篇END   --------------------------------------


# find BEGIN --------------------------------------

# find的运行方式
# 由 logic(-o), \( \), test (比如-name), action(比如 -print) 和 global options(比如depth之类的) 组成
# action都是返回true
# find会拿每一个文件过这个表达式，  触发相应的action, 和普通编程语言的 and/or 逻辑一样
# -prune 相当于直接返回true,  一般会接 -o 让后面的表达式部分无法执行
# 如果整个表达式中(任何地方)没有 -prune 之外的 action, 最后find会自动变成  `\( 跟个表达式 \)` -print
# - 这个会导致一个奇怪的行为
#    - `find .  -name '*.md' -prune` 会打印 "*.md" 文件
#    - 但是如果后面加上一个 -o -print 就会打印相反的文件了

# 学习 https://stackoverflow.com/questions/1489277/how-to-use-prune-option-of-find-in-sh
# 下面那句话只是跑成功了， 我还没有细想过其准确性
find . -maxdepth 1 -mindepth 1 \(  -name v2  -o  -name README.md -o -name r.hd5 -prune -o -exec mv {} v2 \;  \)

# find END   --------------------------------------
