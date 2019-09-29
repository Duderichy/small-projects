import unittest
from main import *
from array import array

class TestFunctions(unittest.TestCase):
    def test_file_max(self):
        self.assertEqual(get_file_max('./tests/unittestdata.csv', 0),
                         ['151860131', '150'])
        self.assertEqual(get_file_max('./tests/unittestdata.csv', 1),
                         ['101843359', '151'])

    def test_file_min(self):
        self.assertEqual(get_file_min('./tests/unittestdata.csv', 0),
                         ['50358597', '150'])
        self.assertEqual(get_file_min('./tests/unittestdata.csv', 1),
                         ['101921163', '42'])

    def test_make_buckets(self):
        self.assertEqual(make_buckets('./tests/unittestdata2.csv', 0, 1),
                         array('i', [0 for _ in range(50 + 42 + 2)]))

    def test_fill_lookup(self):
        self.assertEqual(fill_lookup('./tests/unittestdata3.csv', 0, 1),
                         {10: 3, 11: 3, 12: 3, 13: 4, 14: 6, 15: 7, 16: 7, 17: 7,
                          18: 7, 19: 7, 20: 8, 21: 8, 22: 8, 23: 8, 24: 8, 25: 5,
                          26: 5, 27: 4, 28: 2, 29: 2, 30: 1, 31: 1, 32: 1, 33: 1,
                          34: 1})

if __name__ == "__main__":
    unittest.main()


