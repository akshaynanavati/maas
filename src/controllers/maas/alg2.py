import sys

import config
from controllers.maas import _MaaS
from utils.exceptions import InternalServerError, NotFoundException
from utils.heap import Heap

# Since there are two heaps, we get half as many floats in each buffer
MAX_BUFFER_SIZE = int(config.MEMORY_SIZE * 0.5 / sys.getsizeof(1.0))


class MaaS(_MaaS):
    left_heap = Heap(lambda *args, **kwargs: -cmp(*args, **kwargs), MAX_BUFFER_SIZE)
    right_heap = Heap(cmp, MAX_BUFFER_SIZE)

    @classmethod
    def get_median(cls):
        if cls.left_heap.get_size() == 0 and cls.right_heap.get_size() == 0:
            raise NotFoundException('No items in buffer')
        left_root, right_root = cls.left_heap.get_root(), cls.right_heap.get_root()
        median = None
        if cls.left_heap.get_size() == cls.right_heap.get_size():
            median = (left_root + right_root) / 2
        elif cls.left_heap.get_size() == cls.right_heap.get_size() + 1:
            median = left_root
        elif cls.left_heap.get_size() + 1 == cls.right_heap.get_size():
            median = right_root

        if median is None:
            raise InternalServerError('Heap invariant has been violated')
        else:
            return {'median': median}

    @classmethod
    def reset(cls):
        n = cls.left_heap.get_size() + cls.right_heap.get_size()
        cls.left_heap = Heap(lambda *args, **kwargs: -cmp(*args, **kwargs), MAX_BUFFER_SIZE)
        cls.right_heap = Heap(cmp, MAX_BUFFER_SIZE)
        return {
            'n_deleted': n,
            'max_buffer_size': MAX_BUFFER_SIZE,
            'buffer_size': cls.right_heap.get_size() + cls.left_heap.get_size(),
        }

    @classmethod
    def insert(cls, to_insert):
        assert len(to_insert) <= cls.remaining_space(), 'Buffer full'
        for e in to_insert:
            left_size, right_size = cls.left_heap.get_size(), cls.right_heap.get_size()
            if left_size == 0 and right_size == 0:
                cls.left_heap.insert(e)
                continue
            elif right_size == 0:
                cls.right_heap.insert(e)
                if cls.left_heap.get_root() > cls.right_heap.get_root():
                    cls.left_heap, cls.right_heap = cls.right_heap, cls.left_heap
                continue

            if e < cls.left_heap.get_root():
                insert_heap = cls.left_heap
                other_heap = cls.right_heap
            else:
                insert_heap = cls.right_heap
                other_heap = cls.left_heap

            if insert_heap.get_size() == other_heap.get_size() + 1:
                root = insert_heap.pop_root()
                other_heap.insert(root)
            insert_heap.insert(e)
        return {
            'inserted': to_insert,
            'buffer_size': cls.right_heap.get_size() + cls.left_heap.get_size(),
            'max_buffer_size': MAX_BUFFER_SIZE,
        }

    @classmethod
    def remaining_space(cls):
        return max(0, MAX_BUFFER_SIZE - cls.left_heap.get_size() - cls.right_heap.get_size())

    @classmethod
    def health_check(cls):
        left_size, right_size = cls.left_heap.get_size(), cls.right_heap.get_size()
        if abs(left_size - right_size) > 1:
            raise InternalServerError(
                'Heaps should only differ in size by at most one element.'
            )
        if left_size and right_size and cls.left_heap.get_root() > cls.right_heap.get_root():
            raise InternalServerError(
                'Left heap should have elements smaller than the right heap.'
            )
        return "OK"
