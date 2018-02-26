import threading
import random
import time

# A mutable counter. The object is mutable
# because the methods inc and dec modify self.value

class Counter(object):
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1

    def dec(self):
        self.value -= 1

    def get(self):
        return self.value



class TestThread(threading.Thread):
    def __init__(self, name, testcase, sema, mutex, numrunning):
        threading.Thread.__init__(self, name=name)
        self.testcase = testcase
        self.sema = sema
        self.mutex = mutex
        self.numrunning = numrunning

    def run(self):
        delay = random.random() / 10000.0
        print 'task %s will run for %.1f usec' % (
            self.name, delay * 1e6)

        with self.sema:
            with self.mutex:
                self.numrunning.inc()
                print self.numrunning.get(), 'tasks are running'

            time.sleep(delay)
            print 'task', self.name, 'done'

            with self.mutex:
                self.numrunning.dec()
                print '%s is finished. %d tasks are running' % (
                    self.name, self.numrunning.get())


            
class ThreadTests():

    def test_various_ops(self):
        """ This takes about n/3 seconds
        to complete. n tasks are divided 
        into groups of 3"""

        NUMTASKS = 10
        sema = threading.BoundedSemaphore(value=3)
        mutex = threading.RLock()
        numrunning = Counter()

        threads = []

        for i in range(NUMTASKS):
            t = TestThread("<thread %d>"%i, self, sema, mutex, numrunning)
            threads.append(t)
            yield (t.ident, repr(t))
            t.start()

        print 'waiting for all tasks to complete'
        for t in threads:
            t.join(NUMTASKS)
            yield (t.is_alive(), t.ident, repr(t))
        print 'all tasks done'
        yield (numrunning.get())
