from contextlib import contextmanager
import os

#context manager class to open/close files

class Open_file():
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        f = open(self.filename, self.mode)
        return f

    def __exit__(self, exc_type, exc, exc_tb):
        f.close()

@contextmanager
def open_file_fn(filename, mode):
    f = open(filename, mode)
    yield f
    f.close()
    
@contextmanager
def change_dir_fn(dirname):
    try:
        cwd = os.getcwd()
        os.chdir(dirname)
        yield
    finally:
        os.chdir(cwd)

with Open_file('file1.txt', 'w') as f:
    f.write("This line was written using Open_file class context manager")
#This writes a line in file1.txt

print(f.closed)
#This will print "True"

with open_file_fn('file2.txt', 'w') as f2:
    f2.write("This line was sritten using open_file_fn function based context manager")

print(f2.closed)

with change_dir_fn('/home/ubuntu/dotfiles'):
    print(os.listdir(os.getcwd()))

print(os.getcwd())

