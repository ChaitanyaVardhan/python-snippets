#multiprocessing

from multiprocessing import Pool, Process, Queue, Pipe
import os

def f(x):
    return x*x

def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):
        print 'parent process: {}'.format(os.getppid())
    print 'process id: {}'.format(os.getpid())

def greet_name(name):
    info('function greet_name')
    print 'Hello {}'.format(name)

def f_queue(q):
    q.put(['chaitanya', 'foo', 'bar'])

def f_pipe(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    p1 = Pool(5)
    print (p1.map(f, [1,2,3]))
    p2 = Process(target=greet_name, args=('Chaitanya',))
    p2.start()
    p2.join()

    q = Queue()
    p3 = Process(target=f_queue, args=(q,))
    p3.start()
    print q.get()
    p3.join()

    parent_conn, child_conn = Pipe()
    p4 = Process(target=f_pipe, args=(child_conn,))
    p4.start()
    print parent_conn.recv()
    p4.join()
