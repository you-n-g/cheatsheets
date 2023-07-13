import fire


class BaseRun:

    def __init__(self, a=0):
        self.a = a

    def foo(self, b=0):
        """
        Both the commands below will get the same result ("self.a=10, b=3")
        - `python fire_example.py foo --b 3 --a 10`
        - `python fire_example.py  --a 10 foo --b 3`

        The later parameter will override previous results.
        - `python fire_example.py foo --b 4 --b 3`
        """
        print(f"{self.a=}, {b=}")

    def test_list(self, x):
        """
        following cases will work for list
        - python app/python_apps/fire_example.py test_list good,bad
        - python app/python_apps/fire_example.py test_list '"go-od","bad"'
        - python app/python_apps/fire_example.py test_list '["go-od","bad"]'
        """
        print(x)


if __name__ == "__main__":
    fire.Fire(BaseRun)
    # NOTE: if you want to create subcommand, following commands will be usefule
    # fire.Fire({"base": BaseRun})
