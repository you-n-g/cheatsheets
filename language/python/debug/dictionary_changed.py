from collections import defaultdict

a = defaultdict(list)

a[1].append(3)


try:
    for i in a:
        a[2].append(4)
except Exception as e:
    print(e)


b = {}
b[1] = [3]


try:
    for i in b:
        b[2] = [4]
except Exception as e:
    print(e)
