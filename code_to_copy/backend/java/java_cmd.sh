#!/usr/bin/env bash

# # Outlines: 
# 对jar包的各种操作




# # Outlines: Jar 包相关

jar tf jar-file


# 查看状态
jps  # 查看当前运行的程序 Java Virtual Machine Process Status Tool



# maven
mvn install  # 这个会把要安装的东西都安装好？？？？ 我看一般 package也会生成好的(不包括sourcecode package)，  import marven project 之前需要运行这个
mvn package  # 会在target里生成jar包，然后导入到相应的项目就可以了，  我发现这个和上一个的区别在于会有sourcecode package
# 如果需要调试， 最关键的是安装对的eclipse版本， 然后安装对的市场， 安装maven插件(一般最新版就已经安装好了maven)！ 然后就可以将maven项目导入到eclipse中了

mvn dependency:copy-dependencies -DoutputDirectory=libs  # 会把所有的依赖都拷贝到当前目录？？？？？然后就能用普通方式运行了？？




# 配置java
# 内存相关
-Xmx2048m # 设置大可分配内存



# # Outlines: debug && profiler 相关

# ## Outlines: Debug
# 见init.vim 中的 coc-java-debug && viminspector

# ## Outlines: profiler

# runhprof:
# java 自带的agent， 我没有太看懂
# https://stackoverflow.com/a/10724971

# async-profiler:
# 这个我跑出来了，还画出图来了: 感觉还是不错的
# https://github.com/jvm-profiling-tools/async-profiler

# jvmtop:  
# 可以profiling 正在运行的Java程序
# TODO:  https://stackoverflow.com/a/34887281
