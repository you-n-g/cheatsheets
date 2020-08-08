#!/usr/bin/env python
# -*- coding:utf8 -*-

# save and restore
# http://cv-tricks.com/tensorflow-tutorial/save-restore-tensorflow-models-quick-complete-tutorial/

# save and restore for prediction
# https://datascience.stackexchange.com/questions/16922/using-tensorflow-model-for-prediction

# save and restore 关键是restore之后原来网络的变量名称和现在网络对的上
tf.reset_default_graph()  # 训练完成后我重新设置网络，就不怕名称变化了



# 基本概念
# Graph: tensorflow的计算过程， 描述了数据的流向和计算
# - 可以不显示地指定， 其实等价于 tf.get_default_graph(), g.as_default()
# Session: 和后端的连接， 创建session对象会启动图.
# - sess = tf.Session() 或者 with tf.Session() as sess
# - sess.run #  计算指定的节点: operation 或者 变量
# device: 一般自动指定设备， 也可以手动指定设备
# Variable: tensor, 一般是模型参数
# placeholder : 可以向图中输入数据， 使用feed_dict传输数据
# Operation
# - init_op = tf.global_variables_initializer()  # 这个是用于初始化的operation


# 测试tensorflow gpu计算的benchmark
# https://github.com/tensorflow/benchmarks/tree/master/scripts/tf_cnn_benchmarks
