#!/usr/bin/env python
# coding:utf8



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
    $ nosetests
    If you want to suppress the tensorflow output. Otherwise the logging info will appear in the stdout
    $ nosetests --nologcapture
    If you want to print out the std output, please use command below
    $ nosetests --nocapture

    If you only want to test one case you can specify the file and the method
    $ nosetests test/test_file.py:TestClass.test_method

    Useful options:
    --pdb  Drop into debugger on failures or errors
    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_func(self):
        self.assertSetEqual(True)



if __name__ == '__main__':
    unittest.main()
