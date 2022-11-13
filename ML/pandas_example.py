# %% [markdown]
# # Outlines: view and copy
# https://cloud.tencent.com/developer/article/1653601

import pandas as pd
import numpy as np


df = pd.DataFrame(np.arange(16).reshape(4, 4), index=list('abcd'), columns=list('efbh'))

assert df.loc[:, "e":"f"].values.base is df.values.base   # pandas 的 slice 逻辑和 numpy 一样
assert df.loc[:, ["e", "f"]].values.base is not df.values.base   # pandas 的 slice 逻辑和 numpy 一样

assert df.values.base is df.to_numpy().base

df['x'] = 0.3  #  但是如果变量类型不统一 ， 就不一样了...

assert df.values.base is not df.to_numpy().base

del df["x"]

assert df.values.base is df.to_numpy().base


# %% [markdown]
# ## Outlines: 链式索引

print(df)

df.loc[:, "f":"h"]["h"] = 0   # 链式索引中间出现 引用 赋值成功，  但是出现了warning

print(df)

df.loc[:, ['f', 'h']]['h'] = 1   # 链式索引中间出现了 拷贝 复制失败， 但是没出现warning

print(df)

# 所以这个warning 和是不是用链式索引没关系，  和是不是赋值成功也没关系，  只要中间出现了引用，再出现赋值就会出错

# %% [markdown]
# # Outlines: 拿到view之后， 对原来的df修改会影响view的值

view = df.loc[:, "f":"h"]  # 对view 有影响
print(view)
df['h'] = 10
print(view)

view = df.loc[:, ["f", "h"]]  # 中copy 没有影响
print(view)
df['h'] = 100
print(view)



# %% [markdown]
# # Outlines: Memroy related

import os, psutil
process = psutil.Process(os.getpid())

def get_mem_mb():
    return process.memory_info().rss / 2 ** 20
print(get_mem_mb())

data = pd.DataFrame(np.random.rand(1000 * 1000, 1000))

print(get_mem_mb())

del data

print(get_mem_mb())

data = pd.DataFrame(np.random.rand(1000 * 1000, 1000))

print(get_mem_mb())

data.drop(columns=data.columns, axis=1, inplace=True)

print(get_mem_mb())
data = pd.DataFrame(np.random.rand(1000 * 1000, 1000))


print(data.info(memory_usage="deep"))
