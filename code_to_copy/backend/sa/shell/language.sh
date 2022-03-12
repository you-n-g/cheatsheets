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
}

f 123 123 123123 "{'batch_size': 1024}"

# 有引号空格数量也不一致时， echo $word 和  echo "$word" 是有区别的
a="first        second"
echo $a
echo "$a"
