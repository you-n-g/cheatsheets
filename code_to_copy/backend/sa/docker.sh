#!/usr/bin/env bash




# 使用nsenter访问容器
# docker attach <container> 不好用，多个窗口attach到同一个目录时，因为所有窗口同步显示，所以会阻塞(比如有一个runserver会导致所有都卡在runserver)

# 先安装 >= 2.24 版本的 util-linux，需要用到nsenter
# wget https://www.kernel.org/pub/linux/utils/util-linux/v2.24/util-linux-2.24.tar.bz2
./configure --without-ncurses && make nsenter # 只要用编译生成的nsenter那单个文件就好了

connect_container () {
    PID=$(sudo docker inspect --format "{{ .State.Pid }}" $1)
    nsenter --target $PID --mount --uts --ipc --net --pid
}


# 启动方式
## 常用启动bash方式
docker run -t -i XXX_Repo:XXX_tag /bin/bash
## 常用后台启动方式
docker run -d XXX_Repo:XXX_tag /bin/bash


# 指定container来运行命令
docker exec [OPTIONS] CONTAINER COMMAND
docker exec -t -i CONTAINER bash # 这个是不是就可以代替 nsenter 访问容器了？？


# 查看log
docker logs --tail=20 -f XXX_CONTAINER # 查看container的log



# start起来之后 拷贝文件

# 从host拷贝到container
# 参考 http://stackoverflow.com/questions/22907231/copying-files-from-host-to-docker-container
cp XXX-path-file-host /var/lib/docker/aufs/mnt/XXX_FULL_CONTAINER_ID/XXX_PATH-NEW-FILE 

# 从container拷贝到host
# 参考 http://stackoverflow.com/questions/22049212/docker-copy-file-from-container-to-host
docker cp <containerId>:/file/path/within/container /host/path/target



# 查看信息篇
docker inspect -f '{{.Id}}' XXX_SHORT_ID_or_XXX_NAME # inspect the full id


# container 联网篇
# 最简单的方法是直接用host模式， 这些配置建了新的镜像后就不会存在了
docker  run -it --net=host  ubuntu  /bin/bash


# registry 篇
# 
docker commit <XXX_CONTAINER>  XXX
docker tag XXX_IMAGE XXX_host:5000/XXX_IMAGE # 看来是用tag来描述repo的位置的
docker push XXX_host:5000/XXX_IMAGE
# push可能需要在"/etc/default/docker"加上  DOCKER_OPTS="--insecure-registry XXX_host:5000"
docker pull XXX_host:5000/XXX_IMAGE



