# 和概率相关的一些好玩的脚本

# %% [markdown]
# # Outlines: Gumbel-Max trick

import pandas as pd
import numpy as np

k = 3
n = 10000000
epsilon = np.random.uniform(0, 1, size=(n, k))

a = np.array([1, 2, 3])

argmax = np.argmax(-np.log(-np.log(epsilon)) + np.log(a), axis=1)

vc = pd.Series(argmax).value_counts().sort_index()

delta = (vc / vc.sum()).values - a / np.sum(a)

print(delta)
print(np.isclose(delta, 0, atol=0.001))
