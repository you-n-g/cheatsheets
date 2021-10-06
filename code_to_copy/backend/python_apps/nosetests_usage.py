'''
TODO:
    现在最新的已经切到 pytest了

# pytest -s --pdb
'''

import unittest


def setUpModule():
    # Do sth when enter the module
    pass


def tearDownModule():
    # Do sth when leaving the module
    pass


class TestMultiversoTables(unittest.TestCase):
    '''
    Use the commands below to run test

    # nosetest
    pip install nose

    $ nosetests
    If you want to suppress the tensorflow output. Otherwise the logging info will appear in the stdout
    $ nosetests --nologcapture
    If you want to print out the std output, please use command below
    $ nosetests --nocapture

    If you only want to test one case you can specify the file and the method
    $ nosetests test/test_file.py:TestClass.test_method

    If you want to profiling, please refer to https://stackoverflow.com/a/35563122/443311
    - py-spy is also a good option

    Useful options:
    --pdb  Drop into debugger on failures or errors
    You can install this to enable --ipdb and --ipdb-failures https://github.com/flavioamieiro/nose-ipdb


    If you just want to run this program like normal. You don't have to use nosetest.
    $ python test_file.py TestClass.test_method
    This will not stop the test from printing the stdout


    # pytests
    pip install pytest

    $ python -m pytest .
        or
    $ pytest

    $ pytest --pdb  test/test_file.py:TestClass.test_method
    $ pytest -s ...  #  -s shortcut for --capture=no   #  https://stackoverflow.com/a/14414325

    ## TODO
    [ ] how to hide stdout and std error
    [ ] how to add profiling

    ## 个人体验
    - nosetests好像会错过某些tests, 没找到recursive的选项; pytests 没有这个问题
    - pytest 的测试输出看起来更好看
    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_func(self):
        self.assertSetEqual(True)



if __name__ == '__main__':
    unittest.main()
    # verbosity=100 # 可以看到很多类似的结果




# Coverage 的东西也放在这里了
# pip install coverage
# nosetests --nocapture  --with-coverage --cover-erase --cover-package=market --cover-html
# https://www.saltycrane.com/blog/2012/04/test-coverage-nose-and-coveragepy/
