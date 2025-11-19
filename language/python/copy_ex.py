from copy import deepcopy

x = {}

y = {1: x, 2: x}

x[3] = 3
print(y)


# so the
z = deepcopy(y)

z[1][4] = 4

print("the reference structure is copied in deepcopy")
print(z)

print(y)
