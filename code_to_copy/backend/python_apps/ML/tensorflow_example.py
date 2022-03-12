#!/usr/bin/env python
# -*- coding:utf8 -*-

# # Outlines: 性能问题

# - 下面的在 tensorflow 2.6.2 下测试
import tensorflow as tf

tf.test.is_gpu_available()

# 如果出现了下面的报错， 一般是因为显存不够
#  Internal: Attempting to perform BLAS operation using StreamExecutor without BLAS support


# https://github.com/tensorflow/tensorflow/issues/40261

from tensorflow.keras import Input, Model
from tensorflow.keras.layers import GRU, Dense
import time
import numpy as np

x = Input(shape=(15, 60))

rnn = GRU(50, dropout=0.5, recurrent_dropout=0.5)(x)

y = Dense(1)(rnn)

model = Model(inputs=x, outputs=y)


size, batch = 1000, 50

# 这里期望会 耗时 1.25 秒
t = time.time()
x = model.predict(np.random.rand(size, 15, 60))
# - x 是 numpy array
print("Time for predicting data: ", time.time() - t)


# 这里期望会耗时 0.15秒
t = time.time()
x = model(np.random.rand(size, 15, 60), training=False)
# - x本来的类型: tensorflow.python.framework.ops.EagerTensor
x = np.asarray(x)
print("Time for predicting data: ", time.time() - t)


# 这里期望会耗时 ~0.44秒;
# - 这里慢一点可能是因为它会切成batch
t = time.time()
dataset = tf.data.Dataset.from_tensor_slices(np.random.rand(size, 15, 60)).batch(50)
print("Time for creating data: ", time.time() - t)
x = model.predict(dataset,)
print("Time for predicting data: ", time.time() - t)

# 这里会耗时 1.6 秒
# - 所以手动划batch还是比较慢的
t = time.time()
pred = []
for i in range(size // batch):
    x = model(np.random.rand(batch, 15, 60), training=False)
    # - x本来的类型: tensorflow.python.framework.ops.EagerTensor
    x = np.asarray(x)
    pred.append(x)
pred = np.concatenate(pred)
print("Time for predicting data: ", time.time() - t)

# i = 0
# while i<100:
#     model.predict(np.random.rand(1, 15, 60))
#     i += 1


# # Outlines: random seed
seed = 42

tf.random.set_seed(seed)
v1 = tf.random.uniform((3,)).numpy()
print(v1)

# seed定了，但是不影响接下来的随机
v2 = tf.random.uniform((3,)).numpy()
print(v2)
assert (v2 != v1).any()

# seed运行着再定回来，又能复现数值了
tf.random.set_seed(seed)
v3 = tf.random.uniform((3,)).numpy()
print(v3)
assert (v1 == v3).all()

# 但是这个结果在GPU上无法稳定复现结果 (还不知道怎么复现 tf gpu无法稳定复现的问题)
# 需要借助这个才能稳定复现
# - https://github.com/NVIDIA/framework-determinism


# # Outlines: data


dataset = tf.data.Dataset.range(10)

list(dataset)

# For perfect shuffling, a buffer size greater than or equal to the full size of the dataset is required.
list(dataset.as_numpy_iterator())
assert list(dataset.shuffle(1).as_numpy_iterator()) == list(dataset.as_numpy_iterator())

assert len(dataset.shuffle(2).batch(2)) == len(dataset) / 2   # 如果折半，那么

# 探索多个 iteration shuffle 的性质
X = dataset.shuffle(2)
assert list(X.as_numpy_iterator()) != list(X.as_numpy_iterator())   # 同一个 dataset过多次，顺序是不会被打乱的
x_rep = list(X.repeat(2).as_numpy_iterator())
assert x_rep[:len(x_rep) // 2] != x_rep[len(x_rep) // 2:]   # 用 repeat 也不行

X = dataset.shuffle(2, reshuffle_each_iteration=False)  #  reshuffle_each_iteration 也可以设置成每次都一样
assert list(X.as_numpy_iterator()) == list(X.as_numpy_iterator())   # 同一个 dataset过多次，顺序是不会被打乱的
x_rep = list(X.repeat(2).as_numpy_iterator())
assert x_rep[:len(x_rep) // 2] == x_rep[len(x_rep) // 2:]   # 用 repeat 也不行




# # Outlines: 下面的内容不确定是不是还符合现在新版本

# save and restore
# http://cv-tricks.com/tensorflow-tutorial/save-restore-tensorflow-models-quick-complete-tutorial/

# save and restore for prediction
# https://datascience.stackexchange.com/questions/16922/using-tensorflow-model-for-prediction

# save and restore 关键是restore之后原来网络的变量名称和现在网络对的上
# tf.reset_default_graph()  # 训练完成后我重新设置网络，就不怕名称变化了



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
