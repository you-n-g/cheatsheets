def f():
    """
    >>> print(123)
    123
    >>> print(123)
    1...3
    >>> print(123)
    1...
    """
    # https://docs.python.org/3/library/doctest.html
    # `  # doctest: +ELLIPSIS` seems enabled by default
    # NOTE:
    # Following is not allowed (maybe it can't start with ...)
    # >>> print(123)
    # ...3
    # My vim shortcuts ` rct` ` rt`

