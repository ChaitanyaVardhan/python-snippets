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



def list_valid_subdirs(directory):
    """ returns a list of valid subdirs in a dir"""
    subdirs = []
    for subdir in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, subdir)):
            subdirs.append(subdir)

    return subdirs



def list_valid_filenames_in_directory(directory, white_list_formats,
                                      class_indices, follow_links):
    """List path of files in subdir with extensions in white_list_formats"""
    def _recursive_list(subpath):
        return sorted(os.walk(subpath, followlinks=follow_links))

    classes = []
    filenames = []
    subdir = os.path.basename(directory)
    basedir = os.path.dirname(directory)
    for root, _, files in _recursive_list(directory):
        for fname in sorted(files):
            is_valid = False
            for extension in white_list_formats:
                if fname.lower().endswith('.' + extension):
                    is_valid = True
            if is_valid:
                classes.append(class_indices[subdir])
                absolute_path = os.path.join(root, fname)
                filenames.append(os.path.relpath(absolute_path, basedir))
    return classes, filenames



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



class BuildFileIndex():
    """" builds an index of files present in a directory """
    def __init__(self, directory):
        self.directory = directory
        self.follow_links = False
        cf = CountFiles(self.directory)
        cf.count_files()
        self.samples = cf.count
        classes = list_valid_subdirs(self.directory)
        self.class_indices = dict(zip(classes, range(len(classes))))

    def build_file_index(self):
        self.valid_subdirs = list_valid_subdirs(self.directory)
        pool = multiprocessing.pool.ThreadPool()
        results = []
        self.filenames = []
        self.classes = []
        white_list_formats = ['jpeg', 'jpg', 'png']
        i = 0
        for dirpath in (os.path.join(self.directory, subdir) for subdir in self.valid_subdirs):
            results.append(pool.apply_async(list_valid_filenames_in_directory,
                                            (dirpath, white_list_formats,
                                             self.class_indices, self.follow_links)))
        for res in results:
            classes, filenames = res.get()
            self.classes[i:i + len(classes)] = classes
            self.filenames += filenames
            i += len(classes)
        pool.close()
        pool.join()



class ImageDataGenerator(object):
    def __init__(self):
        "ImageDataGenerator init"

    def flow_from_directory(self, directory, batch_size):
        return DirectoryIterator(directory, self, batch_size)



class Iterator(object):
    def __init__(self, n, batch_size):
        self.n = n
        self.batch_size = batch_size
        self.batch_index = 0
        self.total_batches_seen = 0
        self.index_generator = self._flow_index()

    def reset(self):
        self.batch_index = 0

    def _set_index_array(self):
        self.index_array = range(self.n)


    def _flow_index(self):
        self.reset()
        while 1:
            if self.batch_index == 0:
                self._set_index_array()
            current_index = (self.batch_index * self.batch_size) % self.n
            if self.n > current_index + self.batch_size:
                self.batch_index += 1
            else:
                self.batch_index = 0
            self.total_batches_seen += 1
            yield self.index_array[current_index: current_index + self.batch_size]



class DirectoryIterator(Iterator):
    def __init__(self, directory, image_data_generator, batch_size):
        self.directory = directory
        self.image_data_generator = image_data_generator
        white_list_formats = ['jpeg', 'jpg', 'png']
        self.samples = 0
        bfi = BuildFileIndex(self.directory)
        bfi.build_file_index()
        self.samples = bfi.samples
        self.class_indices = bfi.class_indices
        self.classes = bfi.classes
        self.filenames = bfi.filenames
        super(DirectoryIterator, self).__init__(self.samples, batch_size)



if __name__ == '__main__':
    print count_files_in_directory('/home/ubuntu/dogscats',['jpg', 'jpeg', 'png'])
    CountFiles('/home/ubuntu/dogscats').count_files()
