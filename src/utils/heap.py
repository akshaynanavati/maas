from utils.exceptions import InsufficientStorage


class Heap(object):
    """
    An array heap implementation with log(n) insert, O(1) lookup for the root and log(n) deletion
    of the root.
    """
    def __init__(self, cmp, max_size):
        self.cmp = cmp
        self.heap = [None for _ in xrange(max_size + 1)]
        self.max_size = max_size
        self.leaf_ptr = 1

    def insert(self, elem):
        if self.get_size() == self.max_size:
            raise InsufficientStorage('Heap full')
        self.heap[self.leaf_ptr] = elem
        self.leaf_ptr += 1
        self._rebalance_leaf()

    def pop_root(self):
        root = self.heap[1]
        self.heap[1], self.heap[self.leaf_ptr - 1] = self.heap[self.leaf_ptr - 1], None
        self.leaf_ptr -= 1
        self._rebalance_root()
        return root

    def get_root(self):
        return self.heap[1]

    def get_size(self):
        return self.leaf_ptr - 1

    def _rebalance_leaf(self):
        i = self.leaf_ptr - 1
        while i > 1 and self.cmp(self.heap[i], self.heap[i / 2]) < 0:
            self.heap[i], self.heap[i / 2] = self.heap[i / 2], self.heap[i]
            i /= 2

    def _rebalance_root(self):
        i = 1
        while i < self.leaf_ptr:
            j = i * 2
            if i * 2 < self.leaf_ptr and i * 2 + 1 < self.leaf_ptr:
                if self.cmp(self.heap[i * 2], self.heap[i * 2 + 1]) > 0:
                    j = i * 2 + 1
            elif i * 2 >= self.leaf_ptr:
                break
            if self.cmp(self.heap[i], self.heap[j]) > 0:
                self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
            else:
                break
            i = j
