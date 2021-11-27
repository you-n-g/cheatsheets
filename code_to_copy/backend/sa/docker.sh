#!/usr/bin/env bash



# 启动方式
## 常用启动bash方式
docker run -it --rm XXX_Repo:XXX_tag /bin/bash  # --rm 表示用完自动删除
## 常用后台启动方式
docker run -d XXX_Repo:XXX_tag /bin/bash


# container日常操作篇



# 指定container来运行命令, 但是这个命令只能在containner running的时候才有用。 所以如果你的容器启动的命令是立即退出的，那么可能就只能重新做镜像了。
# 这里有相关的讨论：https://forums.docker.com/t/run-command-in-stopped-container/343/20
docker exec [OPTIONS] CONTAINER COMMAND
docker exec -t -i CONTAINER bash # 这个是不是就可以代替 nsenter 访问容器了？？

# 对于stopped container
docker start -ai XXX_CONTAINER  # 这个命令会让docker重新按原来 run 创建时的命令重新运行。


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
docker rm `docker ps -q -a`  # 删除所有的容器，相应有删除所有的镜像； docker ps 和 images 都支持 -q 参数来只显示 容易/镜像id

sudo docker image rm `sudo docker image list -q -a`


# container 联网篇
# 最简单的方法是直接用host模式， 这些配置建了新的镜像后就不会存在了
docker  run -it --net=host  ubuntu  /bin/bash
 -p 127.0.0.1:$HOSTPORT:$CONTAINERPORT  # 端口映射：在原来镜像的基础上加上这个


# registry 篇
#
docker tag XXX_IMAGE XXX_host:5000/XXX_IMAGE # 看来是用tag来描述repo的位置的
docker push XXX_host:5000/XXX_IMAGE
# push可能需要在"/etc/default/docker"加上  DOCKER_OPTS="--insecure-registry XXX_host:5000"
docker pull XXX_host:5000/XXX_IMAGE

## 制作镜像
docker commit -m "MESSAGE" -a "AUTHOR"  CONTAINER REPO:TAG
# - 如果想挂载volume到已有的镜像，建议commit一次  https://stackoverflow.com/a/33956387
# - REPO:TAG 可以直接换成镜像名字
docker save IMAGE > /tmp/mynewimage.tar   # save Image
docker load < /tmp/mynewimage.tar  # load image

## 相应的有导出和导入容器
docker export <CONTAINER ID> > /home/export.tar  # 用export导出的镜像只有一层，不想save会有很多层
docker import /home/export.tar  REPO:TAG  # 导入只能导成镜像


## 根据dockerfile制作镜像
docker build -f Dockerfiles/Dockerfile.run.tensorflow -t pai.run.tensorflow Dockerfiles/   # -f will use a docker file.   -t will give it a tag
# docker tag pai.run.tensorflow your_docker_registry/pai.run.tensorflow
docker push your_docker_registry/pai.run.tensorflow






# Deprecated

# 使用nsenter访问容器(这个方法是不是已经过时了？？？)
# docker attach <container> 不好用，多个窗口attach到同一个目录时，因为所有窗口同步显示，所以会阻塞(比如有一个runserver会导致所有都卡在runserver)

# 先安装 >= 2.24 版本的 util-linux，需要用到nsenter
# wget https://www.kernel.org/pub/linux/utils/util-linux/v2.24/util-linux-2.24.tar.bz2
./configure --without-ncurses && make nsenter # 只要用编译生成的nsenter那单个文件就好了

connect_container () {
    PID=$(sudo docker inspect --format "{{ .State.Pid }}" $1)
    nsenter --target $PID --mount --uts --ipc --net --pid
}
