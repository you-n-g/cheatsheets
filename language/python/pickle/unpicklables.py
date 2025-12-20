
def f():
    for i in range(10):
        yield i

import pickle

iter = f()

for i in range(4):
    print(next(iter))

s = pickle.dumps(iter)

iter2 = pickle.loads(s)

for i in iter2:
    print(i)
