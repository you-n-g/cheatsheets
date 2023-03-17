#!/bin/sh


# https://stackoverflow.com/a/34531699
while getopts ":yx:a:cd" opt; do
    case $opt in
        a)
        echo "-a was triggered, Parameter: $OPTARG" >&2
        ;;
        c)
        echo "-c was triggered, Parameter: $OPTARG" >&2
        ;;
        d)
        echo "-d was triggered, Parameter: $OPTARG" >&2
        ;;
        \?)
        echo "Invalid option: -$OPTARG" >&2
        exit 1
        ;;
        :)
        echo "Option -$OPTARG requires an argument." >&2
        exit 1
        ;;
    esac
done

# 主要的逻辑是`:?(\w:?)+`:
# - 第一个:控制要不要走报错逻辑(即`\?)`分支)，
#    - 前面(第一个)的 ":" 代表传没有的参数(会当成无参数处理)参数会
#        - 报 `Illegal option -b` 这种错误,
#        - 还是走 `\?)` 分支
# - 后面接(\w:?)+, 一个字母表示一个参数:  字母可以用 ":" 修饰， 后面的 ":" 代表这个要不要接参数
#    - `x:` 代表有参数，但是不一定传
#    - `x` 代表没参数,  只是一个开关
