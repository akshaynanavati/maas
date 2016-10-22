import random
import unittest

from utils import heap
from utils.exceptions import InsufficientStorage


class TestHeap(unittest.TestCase):
    def test_insert(self):
        h = heap.Heap(cmp, 10)
        h.insert(10)
        self.assertEqual(h.get_root(), 10)
        self.assertEqual(h.get_size(), 1)
        h.insert(7)
        self.assertEqual(h.get_root(), 7)
        self.assertEqual(h.get_size(), 2)
        l = range(7)
        random.shuffle(l)
        for i in l:
            h.insert(i)
        self.assertEqual(h.get_root(), 0)
        self.assertEqual(h.get_size(), 9)

    def test_pop(self):
        h = heap.Heap(lambda *args, **kwargs: -cmp(*args, **kwargs), 10)
        l = range(10)
        random.shuffle(l)
        for i in l:
            h.insert(i)
        for i in xrange(9, 0):
            self.assertEqual(h.pop_root(), i + 1)
            self.assertEqual(h.get_root(), i)
            self.assertEqual(h.get_size(), i)

    def test_overflow(self):
        h = heap.Heap(cmp, 10)
        for i in xrange(10):
            h.insert(i)
        with self.assertRaises(InsufficientStorage):
            h.insert(11)
