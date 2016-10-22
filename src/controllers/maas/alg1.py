import sys

import config
from controllers.maas import _MaaS
import utils.alg1 as alg1_utils
from utils.exceptions import NotFoundException, InternalServerError

# Number of floats we can store in memory
MAX_BUFFER_SIZE = int(config.MEMORY_SIZE / sys.getsizeof(1.0))


class MaaS(_MaaS):
    buffer = []
    len_buffer = 0  # cache the length of the buffer

    @classmethod
    def insert(cls, to_insert):
        assert len(to_insert) <= cls.remaining_space(), 'Buffer full'
        cls.buffer.extend(to_insert)
        cls.len_buffer += len(to_insert)
        return {
            'inserted': to_insert,
            'buffer_size': cls.len_buffer,
            'max_buffer_size': MAX_BUFFER_SIZE,
        }

    @classmethod
    def get_median(cls):
        if cls.len_buffer == 0:
            raise NotFoundException('No items in buffer')
        return {
            'median': alg1_utils.median_of_medians(cls.buffer, cls.len_buffer)
        }

    @classmethod
    def reset(cls):
        len_buffer = cls.len_buffer
        cls.buffer = []
        cls.len_buffer = 0
        return {
            'n_deleted': len_buffer,
            'max_buffer_size': MAX_BUFFER_SIZE,
            'buffer_size': cls.len_buffer,
        }

    @classmethod
    def remaining_space(cls):
        return max(0, MAX_BUFFER_SIZE - cls.len_buffer)

    @classmethod
    def health_check(cls):
        if cls.len_buffer != len(cls.buffer):
            raise InternalServerError(
                'Expected buffer size: {} but got {}'.format(len(cls.buffer), cls.len_buffer)
            )
        if cls.len_buffer > MAX_BUFFER_SIZE:
            raise InternalServerError('Buffer size {} is larger than the max size {}'.format(
                cls.len_buffer, MAX_BUFFER_SIZE
            ))
        return 'OK'
