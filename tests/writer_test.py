# from __future__ import absolute_import

import unittest

from common import *

class WriterTest(unittest.TestCase):
    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')

    # def test_create(self):
    #     path = mkdtemp()
    #     generate_database(path, 100)

if __name__ == '__main__':
    unittest.main()