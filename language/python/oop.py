class SuperClassA:
    def __init__(self):
        self.a = 1


class SuperClassB:
    def __init__(self):
        self.b = 1


class SubClass(SuperClassA, SuperClassB):
    def __init__(self):
        super().__init__()


obj = SubClass()

print(dir(obj))  # 会发现python只会按继承顺序找到第一个同名函数（包括__init__）
