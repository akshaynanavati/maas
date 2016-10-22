class _MaaS(object):
    @classmethod
    def insert(cls, to_insert):
        raise NotImplementedError('Child class must implement `insert`')

    @classmethod
    def get_median(cls):
        raise NotImplementedError('Child class must implement `get_median`')

    @classmethod
    def reset(cls):
        raise NotImplementedError('Child class must implement `reset`')

    @classmethod
    def remaining_space(cls):
        raise NotImplementedError('Child class must implement `remaining_space`')

    @classmethod
    def health_check(cls):
        raise NotImplementedError('Child class must implement `health_check`')
