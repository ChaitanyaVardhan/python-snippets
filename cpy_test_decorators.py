"""code in this script adapted from cpython/Lib/test/test_decorators.py"""

def funcattrs(**kwds):
    def decorate(func):
        for key in kwds:
            func.__dict__[key] = kwds[key]
        return func
    return decorate

def foo():
    return 42


if __name__ == '__main__':
    kwds = {'author_name':'Chaitanya'}
    f1 = funcattrs(**kwds)
    f2 = f1(foo)
    print f2
    print foo.__dict__['author_name']
    print f2()

    @funcattrs(**kwds)
    def bar(): return 43
    print bar.__dict__['author_name']
