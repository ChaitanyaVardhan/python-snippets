"""code in this script adapted from cpython/Lib/test/test_decorators.py"""

def funcattrs(**kwds):
    def decorate(func):
        for key in kwds:
            func.__dict__[key] = kwds[key]
        return func
    return decorate

class MiscDecorators:
    @staticmethod
    def author(name):
        def decorate(func):
            func.__dict__['author'] = name
            return func
        return decorate

def memoize(func):
    saved = {}
    def call(*args):
        try:
            return saved[args]
        except KeyError:
            res = func(*args)
            saved[args]= res
            return res
        except TypeError:
            #Unhashable argument
            return func(*args)
    call.func_name = func.func_name
    return call

def countcalls(counts):
    """Decorator to count calls to a function"""
    def decorate(func):
        func_name = func.func_name
        counts[func_name] = 0
        def call(*args, **kwds):
            counts[func_name] += 1
            return func(*args, **kwds)
        call.func_name = func_name
        return call
    return decorate
            
def noteargs(*args, **kwds):
    def decorate(func):
        setattr(func, 'dict_val', (args, kwds))
        return func
    return decorate

def foo():
    return 42

def test_funcattrs():
    kwds = {'author_name':'Chaitanya'}
    f1 = funcattrs(**kwds)
    f2 = f1(foo)
    print f2
    print foo.__dict__['author_name']
    print f2()

    @funcattrs(**kwds)
    def bar(): return 43
    print bar.__dict__['author_name']

def test_MiscDecorators():
    dec1 = MiscDecorators()
    @dec1.author('Vardhan')
    def foo1(): return 44
    print foo1()
    print foo1.__dict__['author']
    print foo1.author

def test_argforms():
    args = ('Now', 'is', 'the', 'time')
    kwds = dict(one=1, two=2)
    @noteargs(*args, **kwds)
    def f3(): return 45
    print f3()
    print f3.dict_val

    @noteargs('follow', 'the', 'money', chapter=7)
    def f4(): return 46
    print f4()
    print f4.dict_val

    @noteargs(1,2,)
    def f3(): pass
    print(f3.dict_val)    

def test_countcalls():
    counts = {}
    
    @countcalls(counts)
    def double(x):
        return x * 2

    #No calls yet
    print counts

    #call 1
    print double(1)
    print counts

    #call 2
    print double(2)
    print counts

def test_memoize():
    counts = {}

    @memoize
    @countcalls(counts)
    def triple(x):
        return x * 3

    #No call yet
    print counts

    #call 1
    print triple(1)
    print counts

    #call 2
    print triple(2)
    print counts

    #call 3
    print triple(2)
    print counts

def test_double():
    print 'Test double'
    class C(object):
        @funcattrs(abc=1, xyz='haha')
        @funcattrs(foobar='oh yeah')
        def foo(self): return 91
    print C().foo()
    print C().foo.abc
    print C().foo.xyz
    print C().foo.foobar

def test_eval_order():
    print "Test eval order"
    actions = []

    def make_decorator(tag):
        actions.append('makedec' + tag)
        def decorate(func):
            actions.append('calldec' + tag)
            return func
        return decorate

    class NameLookupTracer(object):
        def __init__(self, index):
            self.index = index
            
        def __getattr__(self, fname):
            if fname == 'make_decorator':
                opname, res = ('evalname', make_decorator)
            elif fname == 'arg':
                opname, res = ('evalargs', str(self.index))
            else:
                print 'Unknown attrname {}'.format(fname)
            actions.append('%s%d' % (opname, self.index))
            return res

    c1, c2, c3 = map(NameLookupTracer, [1,2,3])
    @c1.make_decorator(c1.arg)
    @c2.make_decorator(c2.arg)
    @c3.make_decorator(c3.arg)
    def foo():
        return 93
    print actions
                    
if __name__ == '__main__':
    test_funcattrs()
    
    test_MiscDecorators()

    test_argforms()

    test_countcalls()

    test_memoize()

    test_double()

    test_eval_order()



    
