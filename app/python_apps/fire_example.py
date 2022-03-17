import fire


class BaseRun:

    def __init__(self, a=0):
        self.a = a

    def foo(self, b=0):
        """
        Both the commands below will get the same result ("self.a=10, b=3")
        - `python fire_example.py foo --b 3 --a 10`
        - `python fire_example.py  --a 10 foo --b 3`
        """
        print(f"{self.a=}, {b=}")


if __name__ == "__main__":
    fire.Fire(BaseRun)
