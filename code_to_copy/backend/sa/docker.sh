#!/usr/bin/env bash




# 使用nsenter访问容器
# docker attach <container> 不好用，多个窗口attach到同一个目录时，因为所有窗口同步显示，所以会阻塞(比如有一个runserver会导致所有都卡在runserver)

# 先安装 >= 2.24 版本的 util-linux，需要用到nsenter
./configure --without-ncurses && make nsenter # 只要用编译生成的nsenter那单个文件就好了

PID=$(sudo docker inspect --format "{{ .State.Pid }}" <XXXcontainer>)
nsenter --target $PID --mount --uts --ipc --net --pid


# 常用启动bash方式
docker run -t -i XXX_Repo:XXX_tag /bin/bash


# 常用后台启动方式
docker run -d XXX_Repo:XXX_tag /bin/bash


