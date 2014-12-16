#!/usr/bin/env bash



# 测试hadoop
bin/hadoop org.apache.hadoop.hdfs.server.namenode.NNThroughputBenchmark -op create -files 200000 -threads $1 &>> ~/log/benchmark_create.log




# 格式化hadoop
bin/hadoop namenode -format




# 将hadoop的程序打包运行
rm -r classes
mkdir classes
javac -cp /XXX_PATH_TO/hadoop-1.2.1/hadoop-core-1.2.1.jar -d classes/  XXX_CLASS_NAME.java
jar -cvf XXX.jar -C ./classes/ .
hadoop jar XXX.jar XXX_CLASS_NAME XXX_INPUT XXX_OUTPUT
