#code in this file adapted from cpython/Lib/test/test_iter.py

import unittest

TRIPLETS = [(0,0,0), (0,0,1), (0,0,2),
            (0,1,0), (0,1,1), (0,1,2),
            (0,2,0), (0,2,1), (0,2,2),

            (1,0,0), (1,0,1), (1,0,2),
            (1,1,0), (1,1,1), (1,1,2),
            (1,2,0), (1,2,1), (1,2,2),

            (2,0,0), (2,1,1), (2,1,2),
            (2,1,0), (2,1,1), (2,1,2),
            (2,2,0), (2,2,1), (2,2,2)]

class BasicIterClass:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def next(self):
        res = self.i
        if res > self.n:
            raise StopIteration
        self.i = res + 1
        return res

class IteratingSequenceClass:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return BasicIterClass(self.n)


class SequenceClass:
    def __init__(self, n):
        self.n = n

    def __getitem__(self, i):
        if 0 <= i < self.n:
            return i
        else:
            raise IndexError

class TestIterator():
    def check_iterator(self, it, seq):
        self.res = []
        while 1:
            try:
                val = it.next()
            except StopIteration:
                break
            self.res.append(val)

    #Test basic use of iter() function
    def test_iter_basic(self):
        self.check_iterator(iter(range(10)), range(10))

    def test_iter_idempotency(self):
        seq = range(10)
        it = iter(seq)
        it2 = iter(seq)
        return it, it2
