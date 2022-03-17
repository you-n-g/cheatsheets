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
