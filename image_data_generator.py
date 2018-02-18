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



class DirectoryIterator:
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

            

