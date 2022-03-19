#!/bin/sh

# 和语法相关的一些cheatsheet在这里


# function f() {}  is not supported in pure `sh`
f() {
    # shell函数取参数
    # http://stackoverflow.com/questions/12314451/accessing-bash-command-line-args-vs
    # for 循环时会有大量的不同

    echo '$* 和 $@ 会把你引号包住的全拆开'
    for i in $@
    do
        echo "[$i]"
    done

    for i in $*
    do
        echo "[$i]"
    done

    echo '"$@" 常常是我们想要的， 引号包住的在一起， 该分开的分开'
    for i in "$@"
    do
        echo "[$i]"
    done

    echo '"$*" 会把各个段都合并成一个'
    for i in "$*"
    do
        echo "[$i]"
    done
    
    # 可以对参数做一些判断
    if [[ "$@" == *"batch_size"* ]]; then
        echo "batch_size detected"
    fi

    if [[ "$@" == *"rubbish"* ]]; then
        echo "rubbish detected"
    fi
}

f 123 123 123123 "{'batch_size': 1024}"

# 有引号空格数量也不一致时， echo $word 和  echo "$word" 是有区别的
a="first        second"
echo $a
echo "$a"


# # Outlines: 一些符号的区别

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

# ## Outlines: 单括号和双括号的区别
## if 从句中， 不同的命令可以用  ！ -a -o  之类的逻辑运算符连接
## - [  ] 本质是test，也算命令的一种， 可以和其他命令用逻辑运算链接
DEBUG=0

# if [ $DEBUG eq 0 ] ; then  # this is wrong
# if [ $DEBUG eq 0 ] ; then  # this is wrong
# if [ $DEBUG -lt 10 ] ; then  # this is right
if  test $DEBUG -lt 10 ; then  # this is right; 这个和上面是等价的
    echo True single lt
fi

# if [ $DEBUG < 10 ] ; then   #  这里会得到 `10: No such file or directory` 这个错误， 可以看出它完全是把解释成 shell在用
#     echo True
# fi

if [ "abc" = *"b"* ] ; then  #  单括号很自然就没有用啦; sh 不支持通配符
    echo "String compare works single"
fi
# - 如果想上述case也有用，那么请参照 https://stackoverflow.com/a/19897118 (一个特别绕的例子)


if [[ "abc" = *"b"* ]] ; then  #  双括号很自然就没有用啦
    echo "String compare works double"
fi

# 双中括号是更高级的语法
# NOTE: 但是对 sh 完全不兼容；  会得到 `[[: not found` 这种错误
if [[ $DEBUG < 10 ]] ; then
    echo True
fi

if [[ $DEBUG -eq 0 ]] ; then  # 而且对单括号的兼容性也不错
    echo True eq
fi
