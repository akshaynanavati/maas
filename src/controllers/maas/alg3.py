import sys

import config
from controllers.maas import _MaaS
from utils.exceptions import NotFoundException

# Number of ints we can store in memory
MAX_BUFFER_SIZE = int(config.MEMORY_SIZE / sys.getsizeof(1))
BUCKET_SIZE = 1


class MaaS(_MaaS):
    frequency_map = [0 for _ in xrange(MAX_BUFFER_SIZE)]
    n = 0
    min_index = None

    @classmethod
    def get_median(cls):
        if cls.n == 0:
            raise NotFoundException('No items in buffer')
        target = cls.n / 2
        count = 0
        for e in xrange(cls.min_index, MAX_BUFFER_SIZE):
            freq = cls.frequency_map[e]
            if count + freq >= target:
                median_position = freq - (target - count)
                return {'median': 1.0 * median_position / (freq + 1) + e * BUCKET_SIZE}
            count += freq

    @classmethod
    def reset(cls):
        n = cls.n
        cls.frequency_map = [0 for _ in xrange(MAX_BUFFER_SIZE)]
        cls.n = 0
        cls.min_index = None
        return {
            'n_deleted': n,
            'upper_bound': MAX_BUFFER_SIZE * BUCKET_SIZE,
            'buffer_size': cls.n,
            'bucket_size': BUCKET_SIZE,
        }

    @classmethod
    def insert(cls, to_insert):
        for e in to_insert:
            e /= BUCKET_SIZE
            # Bucket all values larger than our max into the max bucket
            if e >= MAX_BUFFER_SIZE:
                e = MAX_BUFFER_SIZE - 1
            cls.frequency_map[int(e)] += 1
            cls.n += 1
            if cls.min_index is None:
                cls.min_index = int(e)
            else:
                cls.min_index = min(cls.min_index, int(e))
        return {
            'inserted': to_insert,
            'upper_bound': MAX_BUFFER_SIZE * BUCKET_SIZE,
            'buffer_size': cls.n,
            'bucket_size': BUCKET_SIZE,
        }

    @classmethod
    def remaining_space(cls):
        return sys.maxint

    @classmethod
    def health_check(cls):
        return 'OK'
