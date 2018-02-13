#code in this file adapted from cpython/Lib/test/test_iter.py

import unittest

import os

TRIPLETS = [(0,0,0), (0,0,1), (0,0,2),
            (0,1,0), (0,1,1), (0,1,2),
            (0,2,0), (0,2,1), (0,2,2),

            (1,0,0), (1,0,1), (1,0,2),
            (1,1,0), (1,1,1), (1,1,2),
            (1,2,0), (1,2,1), (1,2,2),

            (2,0,0), (2,1,1), (2,1,2),
            (2,1,0), (2,1,1), (2,1,2),
            (2,2,0), (2,2,1), (2,2,2)]

TESTFN = "testfile.txt"

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
    def check_iterator(self, it):
        res = []
        while 1:
            try:
                val = it.next()
            except StopIteration:
                break
            res.append(val)
        return res

    def check_for_loop(self, it):
        res = []
        for i in it:
            res.append(i)
        return res
            
    #Test basic use of iter() function
    def test_iter_basic(self):
        res = self.check_iterator(iter(range(10)))
        return res

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

    #check explicit iter on a class with __iter__
    def test_iter_class_iter(self):
        res = self.check_iterator(iter(IteratingSequenceClass(10)))
        return res

    #check iter on a sequence class without iter
    def test_seq_class_iter(self):
        res = self.check_iterator(iter(SequenceClass(10)))
        return res

    #check for loop on a sequence class without __iter__
    def test_seq_class_for(self):
        res = self.check_for_loop(SequenceClass(10))
        return res

    def test_mutating_seq_class_exhausted_iter(self):
        a = SequenceClass(5)
        it1 = iter(a)
        it2 = iter(a)
        for x in it1:
            next(it2)
        a.n = 7
        return(list(it1), list(it2), list(a))

    def test_new_style_iter_class(self):
        class IterClass(object):
            def __iter__(self):
                return self

        return IterClass()

    # test 2 argument iter with a callable instance
    def test_iter_callable(self):
        class C:
            def __init__(self):
                self.i = 0
            def __call__(self):
                i = self.i
                self.i = i + 1
                if i > 100:
                    raise IndexError
                return i
        return(iter(C(), 20))

    # test 2 argument iter() with a function
    def test_iter_function(self):
        def spam(state=[0]):
            i = state[0]
            state[0] = i + 1
            return i
        return(iter(spam, 20))

    # test 2 argument iter() with a function that raises StopIteration
    def test_iter_function_stop(self):
        def spam(state=[0]):
            i = state[0]
            if i == 10:
                raise StopIteration
            state[0] = i + 1
            return i
        return (iter(spam, 20))

    # test exception propagation through function iterator
    def test_exception_function(self):
        def spam(state=[0]):
            i = state[0]
            state[0] = i + 1
            if i == 10:
                raise RuntimeError
            return i
        res = []
        try:
            for x in iter(spam, 20):
                res.append(x)
        except RuntimeError:
            return len(res)
        else:
            return "Should have raised RuntimeError"

    # test exception propagation through sequence iterator
    def test_exception_sequence(self):
        class MySequenceClass(SequenceClass):
            def __getitem__(self, i):
                if i == 10:
                    raise RuntimeError
                return SequenceClass.__getitem__(self, i)
        res = []
        try:
            for x in MySequenceClass(20):
                res.append(x)
        except RuntimeError:
            return res

    # Test a big range
    def test_a_big_range(self):
        return self.check_for_loop(iter(range(10000)))

    # Test an empty list
    def test_iter_empty(self):
        return self.check_for_loop(iter([]))

    # Test an xrange
    def test_iter_xrange(self):
        return self.check_for_loop(iter(xrange(10)))

    #Test a string
    def test_iter_string(self):
        return self.check_for_loop(iter("abcde"))

    #Test a dictionary
    def test_iter_dict(self):
        dict = {}
        for i in range(10):
            dict[i] = None
        self.check_for_loop(dict)

    # Test a file
    def test_iter_file(self):
        f = open(TESTFN, "w")
        try:
            for i in range(5):
                f.write("%d\n" % i)
        finally:
            f.close()
        f = open(TESTFN, "r")
        try:
            res1 = self.check_for_loop(f)
            yield res1
        finally:
            f.close()
            try:
                os.unlink(TESTFN)
            except OSError:
                pass

    # Test list()'s use of iterator
    def test_builtin_list(self):
        f = open(TESTFN, "w")
        try:
            for i in range(11):
                f.write("%d\n" % i)
        finally:
            f.close()
        f = open(TESTFN, "r")
        try:
            res1 = self.check_for_loop(list(f))
            yield res1
            f.seek(2,0)
            res2 = self.check_for_loop(list(f))
            yield res2
        finally:
            f.close()
            try:
                os.unlink(TESTFN)
            except OSError:
                pass

    # Test tuple()'s use of iterator
    def test_builtin_tuple(self):
        f = open(TESTFN, "w")
        try:
            for i in range(12):
                f.write("%d\n" % i)
        finally:
            f.close()
        f = open(TESTFN, "r")
        try:
            res1 = self.check_for_loop(tuple(f))
            yield res1
            f.seek(-2, 1)
            res2 = self.check_for_loop(tuple(f))
            yield res2
        finally:
            f.close()
            try:
                os.unlink(TESTFN)
            except OSError:
                pass

    # Test filter()'s use of iterators
    def test_builtin_filter(self):
        class Boolean:
            def __init__(self, truth):
                self.truth = truth
            def __nonzero__(self):
                return self.truth
        bTrue = Boolean(1)
        bFalse = Boolean(0)

        class Seq:
            def __init__(self, *args):
                self.vals = args
            def __iter__(self):
                class SeqIter:
                    def __init__(self, vals):
                        self.vals = vals
                        self.i = 0
                    def __iter__(self):
                        return self
                    def next(self):
                        i = self.i
                        self.i = i + 1
                        if i < len(self.vals):
                            return self.vals[i]
                        else:
                            raise StopIteration
                return SeqIter(self.vals)

        seq = Seq(*([bTrue, bFalse] * 25))
        res1 = filter(lambda x: not x, seq)
        yield res1
        res2 = filter(lambda x: not x, iter(seq))
        yield res2
