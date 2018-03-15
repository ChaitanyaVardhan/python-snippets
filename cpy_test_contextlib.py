"""Code in this file adapted from cpython/Lib/test/test_contextlib.py"""

from contextlib import *

def test_context_manager_plain():
    state = []
    @contextmanager
    def woohoo():
        state.append(1)
        yield 40
        state.append(999)

    with woohoo() as x:
        print state
        print x
        state.append(x)
        print state

def test_context_manager_finally():
    state = []

    @contextmanager
    def f_finally():
        state.append(1)
        try:
            yield 42
        finally:
            state.append(999)

    with f_finally() as context_f1:
        print state
        print context_f1
        state.append(context_f1)
    print state

def test_keywords():
    @contextmanager
    def weehee(self, func, args, kwds):
        yield (self, func, args, kwds)

    with weehee(self=11, func=12, args=13, kwds=14) as target:
        print target

if __name__ == '__main__':
    print 'test_context_manager_plain'
    test_context_manager_plain()

    print 'test_keywords'
    test_keywords()

    print 'test_context_manager_finally'
    test_context_manager_finally()


