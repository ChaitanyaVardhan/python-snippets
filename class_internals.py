class Counter:
    def __init__(self, lo, hi):
        self.hi = hi
        self.lo = lo

    def __iter__(self):
        return self

    def next(self):
        value = self.lo
        if self.lo > self.hi:
            raise StopIteration
        self.lo += 1
        return value

c1 = Counter(2,20)
for c in c1:
    print c

