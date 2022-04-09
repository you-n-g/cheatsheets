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

# 主要的逻辑是:
# - 一个字母表示一个参数
# - 字母可以用 ":" 修饰， 后面的 ":" 代表这个要不要接参数，  前面的 ":" 代表没有传参会不会走报错逻辑 ":)"
