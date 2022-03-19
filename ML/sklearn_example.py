import numpy as np
from sklearn.model_selection import KFold
y = np.arange(30)
kf = KFold(n_splits=2, shuffle=True)
kf.get_n_splits(y)

for train_index, test_index in kf.split(y):
    print("TRAIN:", train_index, "TEST:", test_index)
    y_train, y_test = y[train_index], y[test_index]
    # NOTE: 所有的序都是保留的！！
    assert (train_index == sorted(train_index)).all()
    assert (test_index == sorted(test_index)).all()


from sklearn.model_selection import StratifiedKFold
x = np.arange(10)
y = np.array([0, 1]).repeat(5)
skf = StratifiedKFold(n_splits=2, shuffle=True)
skf.get_n_splits(x, y)

print(skf)
for train_index, test_index in skf.split(x, y):
    print("TRAIN:", train_index, "TEST:", test_index)
    x_train, x_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]
    # 同样，这里也是保全了所有的序
    assert (x_train == sorted(x_train)).all()
    assert (x_test == sorted(x_test)).all()
