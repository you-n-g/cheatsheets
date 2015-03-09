#!/usr/bin/env bash
awk '{print $2}'


# 文本处理
# 在匹配到的某行后再加一行, 自己举一反三得到 /i 怎么用
sed -i '/LINE_XXX_PATTERN/a XXX_CONTENT' XXX_FILE
sed -i '1d' # 删除第一行

# sed 每次处理一行，先选择， 后接命令
