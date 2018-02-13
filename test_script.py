import cpython_iterator as cpi

import sys

ti = cpi.TestIterator()

def build_func(func_name):
    def f():
        return func_name
    return f

def test():
    print "Hello from test"

if __name__ == '__main__':
    print sys.argv
    func_name = sys.argv[1]+'()'
    print 'executing {}'.format(func_name)
    func = build_func(func_name)
    func()
