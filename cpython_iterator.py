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

    def check_for_loop(self, it):
        res = []
        for i in it:
            res.append(i)
        return res
            
    #Test basic use of iter() function
    def test_iter_basic(self):
        self.check_iterator(iter(range(10)), range(10))

    #test iter(x) and iter(iter(x)) are same
    def test_iter_idempotency(self):
        seq = range(10)
        it = iter(seq)
        it2 = iter(seq)
        return it, it2

    #test that for loop works over iterator
    def test_iter_for_loop(self):
        res = self.check_for_loop(iter(range(10)))
        return res

    #test iter independence over the same list
    def test_iter_independence(self):
        seq = range(3)
        res = []
        for i in iter(seq):
            for j in iter(seq):
                for k in iter(seq):
                    res.append((i,j,k))
        return res

    #test nested list comp on iter
    def test_nested_comp_iter(self):
        seq = range(3)
        res = [(i,j,k) for i in iter(seq) for j in iter(seq) for k in iter(seq)]
        return res

    #test nested comp without iter
    def test_comp_for(self):
        seq = range(3)
        res = [(i,j,k) for i in seq for j in seq for k in seq]
        return res

    #test for loop for a class with __iter__
    def test_iter_class_for(self):
        res = self.check_for_loop(IteratingSequenceClass(10))
        return res




