#code adapted from keras/keras/preprocessing/image.py

import os
import multiprocessing.pool
from functools import partial

class ImageDataGenerator:
    def __init__(self):
        pass

    def flow_from_directory(self, directory, batch_size):
        return DirectoryIterator(
            directory,
            self,
            batch_size)



def _count_valid_files_in_directory(directory, white_list_formats, follow_links):
    """ count files with extension in white_list_formats """
    def _recursive_list(subpath):
        return sorted(os.walk(subpath, followlinks=follow_links), key=lambda x: x[0])

    samples = 0
    for _,_, files in _recursive_list(directory):
        for fname in files:
            is_valid = False
            for extension in white_list_formats:
                if fname.lower().endswith('.' + extension):
                    is_valid = True
                    break
            if is_valid:
                samples += 1
    return samples



class Iterator(object):
    """Base class for iterators
    Arguments: 
    n: Integer, total number of samples in a dataset to loop over
    batch_size: Integer, size of a batch
    """

    def __init__(self, n, batch_size):
        self.n = n
        self.batch_size = batch_size
        self.index_generator = self._flow_index()

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
            yield self.index_array[current_index:
                                   current_index + self.batch_size]

    def reset(self):
        self.batch_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.next()

    def _get_batches_of_transformed_samples(self, index_array):
        raise NotImplementedError

class DirectoryIterator(Iterator):
    def __init__(self,
                 directory,
                 image_data_generator,
                 batch_size=32,
                 classes=None,
                 follow_links=False):
        self.directory = directory
        self.image_data_generator = image_data_generator
        self.classes = classes

        white_list_formats = {'png', 'jpg', 'jpeg', 'bmp'}

        self.samples = 0

        if not classes:
            classes = []
            for subdir in sorted(os.listdir(directory)):
                if os.path.isdir(os.path.join(directory, subdir)):
                    classes.append(subdir)
        self.num_classes = len(classes)
        self.class_indices = dict(zip(classes, range(len(classes))))

        pool = multiprocessing.pool.ThreadPool()
        function_partial = partial(_count_valid_files_in_directory,
                                   white_list_formats=white_list_formats,
                                   follow_links=follow_links)
        self.samples = sum(pool.map(function_partial, 
                                    (os.path.join(directory, subdir)
                                     for subdir in classes)))
        print('Found {} images belonging to {} classes'.format(self.samples,
                                                               self.num_classes))

        results = []

        self.filenames = []
        self.classes = [2%2 for i in range(self.samples)]
        i = 0
        for dirpath in (os.path.join(directory, subdir) for subdir in classes):
            results.append(pool.apply_async(_list_valid_filenames_in_directory,
                                            (dirpath, white_list_formats,
                                             self.class_indices, follow_links)))

        for res in results:
            classes, filenames = res.get()
            self.classes[i:i + len(classes)] = classes
            self.filenames += filenames
            i += len(classes)
        pool.close()
        pool.join()
        super(DirectoryIterator, self).__init__(self.samples, batch_size)
        
            

            

