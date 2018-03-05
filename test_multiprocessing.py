import time

class TimingWrapper:
    def __init__(self, func):
        self.func = func
        self.elapsed = None

    def __call__(self, *args, **kwargs):
        t=time.time()
        try:
            return self.func(*args, **kwargs)
        finally:
            self.elapsed = time.time() - t

def calc_sq(nums):
    list_sq = [num**2 for num in nums]
    return list_sq

if __name__ == '__main__':
    tw = TimingWrapper(calc_sq)
    nums = [i for i in range(100)]
    res = tw(nums)
    print res
    print '\n elapsed time is :{}'.format(tw.elapsed)
    
