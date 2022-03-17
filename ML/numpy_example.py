# TODO: 把 scipy.py 中numpy相关的内容拿出来



# %% [markdown]
# # Outlines: view and copy
# view and copy: https://cloud.tencent.com/developer/article/1653601

import numpy as np

arr = np.array([1, 2, 4, 8, 16, 32])

view_of_arr = arr[1:4:2]

# %% [markdown]
# ## Outlines: 怎么看是不是view
assert arr.base is None
assert view_of_arr.base is arr

assert arr.flags.owndata is True
assert view_of_arr.flags.owndata is False

assert arr.nbytes ==  8 * 6
assert view_of_arr.nbytes  == 8 * 2

from sys import getsizeof
getsizeof(arr)
getsizeof(view_of_arr)


# %% [markdown]
# ## Outlines: 修改会造成什么变化
arr[1] = 100

view_of_arr  # view 会因为源 arr 改变而变化

view_of_arr[0] = 1000

arr  # 改view 也会影响原arr

# %% [markdown]
# ## Outlines: index 和 mask 是拷贝

assert arr[1:3].flags.owndata is False

assert arr[[1,3]].flags.owndata is True
assert arr[[True, True, False, True, False, True]].flags.owndata is True

arr[[1]][0] = 100000
assert arr[[1]][0] != 100000   # 注意拷贝 赋值不会对原来有影响；

arr[1:2][0] = 100000
assert arr[1:2][0] == 100000  # 但是view会


# %% [markdown]
# ## Outlines: header

_arr2d = np.arange(16)
arr2d = _arr2d.reshape(4, 4)

assert arr2d.flags.owndata is False    # reshape 也会变成view

assert arr2d[0].flags.owndata is False

assert arr2d[0].base is arr2d.base
