#codes in this files are inspired from the keras source code 
# https://github.com/keras-team/keras

import os
import multiprocessing.pool
from functools import partial

def count_files_in_directory(dirpath, white_list_formats):
    """counts the files of a some format(jpeg, jpg etc.)
    that are present in subdirectories of a directory"""
    def recursive_list(dirpath):
        return sorted(os.walk(dirpath))

    count = 0
    for _, _, files in recursive_list(dirpath):
        for fname in files:
            is_valid = False
            for format in white_list_formats:
                if fname.lower().endswith('.' + format):
                    is_valid = True
                    break
            if is_valid == True:
                count += 1
    return count

class CountFiles(object):
    def __init__(self, directory):
        self.directory  = directory
        self.white_list_formats = ['jpeg', 'jpg', 'png']
        self.valid_subdirs = []
        self.count = 0
        for subdir in os.listdir(self.directory):
            if os.path.isdir(os.path.join(self.directory, subdir)):
                self.valid_subdirs.append(subdir)

    def count_files(self):
        function_partial = partial(count_files_in_directory, white_list_formats=self.white_list_formats)
        pool = multiprocessing.pool.ThreadPool()
        self.count = sum(pool.map(function_partial, (os.path.join(self.directory, subdir)
                                                             for subdir in self.valid_subdirs)))

        print 'Found {} files in {} subdirectories '.format(self.count, len(self.valid_subdirs))

if __name__ == '__main__':
    print count_files_in_directory('/home/ubuntu/dogscats',['jpg', 'jpeg', 'png'])
    CountFiles('/home/ubuntu/dogscats').count_files()
