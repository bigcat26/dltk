from os import rmdir
from tempfile import mkdtemp
import unittest
from tempfile import mkdtemp
from common import generate_database
import shutil

import dltk

class ReaderTest(unittest.TestCase):
    def setUp(self):
        self.db_records = 20
        self.db_path = mkdtemp()
        generate_database(self.db_path, self.db_records)
        print(f'setUp database={self.db_path}')

    def tearDown(self):
        print(f'tearDown database={self.db_path}')
        shutil.rmtree(self.db_path)

    def test_load(self):
        print(f'test_load database={self.db_path}')
        with dltk.LMDBDatabaseReader(self.db_path) as reader:
            self.assertEqual(self.db_records, len(reader))

    def test_split(self):
        print(f'test_split database={self.db_path}')
        with dltk.LMDBDatabaseReader(self.db_path) as reader:
            origin_length = len(reader)

            ratio = [0.8, 0.2]
            datasets = reader.split(ratio)
            self.assertEqual(origin_length * 0.8, len(datasets[0]))
            self.assertEqual(origin_length * 0.2, len(datasets[1]))

            ratio = [0.3, 0.3, 0.4]
            datasets = reader.split(ratio)
            self.assertEqual(origin_length * 0.3, len(datasets[0]))
            self.assertEqual(origin_length * 0.3, len(datasets[1]))
            self.assertEqual(origin_length * 0.4, len(datasets[2]))

    # def test_version(self):
    #     ver = lmdb.version()
    #     assert len(ver) == 3
    #     assert all(isinstance(i, INT_TYPES) for i in ver)
    #     assert all(i >= 0 for i in ver)

    # def test_version_subpatch(self):
    #     ver = lmdb.version(subpatch=True)
    #     assert len(ver) == 4
    #     assert all(isinstance(i, INT_TYPES) for i in ver)
    #     assert all(i >= 0 for i in ver)
