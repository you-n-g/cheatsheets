#!/usr/bin/env bash



# ## Outlines: awk

awk '{print $2}'
# cheatsheets: https://coolshell.cn/articles/9070.html



# ## Outlines: sed

# 文本处理
# 在匹配到的某行后再加一行, 自己举一反三得到 /i 怎么用
sed -i '/LINE_XXX_PATTERN/a XXX_CONTENT' XXX_FILE
sed -i '1d' # 删除第一行
sed -i '0,/port=-1/{s/port=-1/port=ask-1/}' /etc/xrdp/xrdp.ini  # 找到第一个port=-1, 执行中括号里面的命令   https://stackoverflow.com/a/9453461

sed -i '$ a 10.0.0.23:/datadrive01/shared_nfs/ /data/nfs_5T/ nfs    auto  0  0'  # 在最后一行添加内容，可以避免使用管道(回避权限问题)

# sed 每次处理一行，先选择， 后接命令
# cheatsheets: https://coolshell.cn/articles/9104.html



# ## Outlines: awk
awk -f  # awk会根据自己认识的类型过滤文件， 所以提供了先看文件列表的方式
ack <STH> --pager="less -R"  # 可以在less中有高亮地看结果
ack <STH> -w  # 可以直接按work匹配

# TODO: ackrc，  看看这里面能不能设置一下文件类型
# 加入更多的 filetype:  https://stackoverflow.com/a/3871324

# cheatsheets
# https://kapeli.com/cheat_sheets/Ack.docset/Contents/Resources/Documents/index



# ## Outlines: Miscellaneous
XXX | sort -k N  # 按第n列排序， 比如看日志时按时间排序！！！

tr '\n' ' ' # 把字符换成空格
tr -d '\n' # 把换行删掉

