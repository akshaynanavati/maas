def _median_of_medians(l, start, end, k):
    """
    An O(n) divide and conquer algorithm to compute the median of an unsorted list.

    :param l: an unsorted list of floats.
    :param start: starting index of list l
    :param end: ending index of list l
    :param k: the kth element to return

    :return: the kth smallest element from ``l[start:end]``
    """
    assert start < end
    n = end - start
    assert k < n, 'Cannot find {}th smallest element in a list of size {}'.format(k, n)
    if n < 6:
        return sorted(l[start:end])[k]
    medians = []
    for i in xrange(0, n, 5):
        if i + 5 <= n:
            medians.append(_median_of_medians(l, i, i + 5, 2))
        else:
            medians.append(_median_of_medians(l, i, n, (n - i) / 2))
    median = _median_of_medians(medians, 0, len(medians), (len(medians)) / 2)
    left, right = partition(l, start, end, median)
    assert len(left) + len(right) == n
    if len(left) == k:
        return median
    elif len(left) < k:
        return _median_of_medians(right, 0, len(right), k - len(left))
    else:
        return _median_of_medians(left, 0, len(left), k)


def partition(l, start, end, p):
    """
    Partitions the list ``l[start:end]`` on the pivot ``p``

    :param l: list of floats
    :param start: start index of l
    :param end: end index of l
    :param p: pivot

    :return: ``left``, ``right`` such that left is all elements in ``l[start:end]`` that are \
        smaller than ``p`` and right is all elements in ``l[start:end]`` that are larger than ``p``.
    """
    assert start < end
    left, right = [], []
    for i in xrange(start, end):  # Avoid making a copy of the list here
        if l[i] < p:
            left.append(l[i])
        else:
            right.append(l[i])
    return left, right


def median_of_medians(l, n):
    return _median_of_medians(l, 0, n, n / 2)
