import random
import unittest

from utils.alg1 import median_of_medians, partition


class TestMedianOfMedians(unittest.TestCase):
    def test_median_of_medians(self):
        l = range(100)
        random.shuffle(l)
        self.assertEqual(median_of_medians(l, len(l)), range(100)[50])
        l = [7, 3, 5]
        self.assertEqual(median_of_medians(l, 3), 5)
        l = range(101)
        random.shuffle(l)
        self.assertEqual(median_of_medians(l, len(l)), range(101)[50])
        l = [random.random() for _ in xrange(11)]
        median = sorted(l)[5]
        self.assertEqual(median_of_medians(l, 11), median)

    def test_partition(self):
        self.assertEqual(partition(range(10), 0, 10, 5), ([0, 1, 2, 3, 4], [5, 6, 7, 8, 9]))
        l = range(10)
        self.assertEqual(partition(l, 3, 5, 5), ([3, 4], []))
        with self.assertRaises(AssertionError):
            partition([12, 3], 5, 1, 10)
