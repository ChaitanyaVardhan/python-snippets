#codes in this files are inspired from the keras source code 
# https://github.com/keras-team/keras

def count_files_in_directory():
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
            if is_valid = True:
                count += 1
    return count

if __name__ == '__main__':
    directory = ''
    white_list_formats = ['jpeg', 'jpg', 'png']
    print count_files_in_directory(directory, white_list_formats)

