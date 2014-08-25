#!/usr/bin/env bash



# 测试hadoop
bin/hadoop org.apache.hadoop.hdfs.server.namenode.NNThroughputBenchmark -op create -files 200000 -threads $1 &>> ~/log/benchmark_create.log




# 格式化hadoop
bin/hadoop namenode -format

