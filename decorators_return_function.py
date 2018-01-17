def surround_with(surrounding):
    """return a function with the *surrounding* passed to it"""
    def surround_word(word):
        return " {}{}{}".format(surrounding, word, surrounding)
    return surround_word

def transform_string(input_string, targets, transform_fn):
    """transforms an input string by surroundig the words in the string 
        present in the target list"""
    result = ''
    for word in input_string.split():
        if word in targets:
            result += ' {}'.format(transform_fn(word))
        else:
            result += ' {}'.format(word)

    return result

if __name__ == '__main__':
    input_string = 'My name is Chaitanya Vardhan and I love the Python languange and I have watched the Anaconda movie too'
    targets = ['Chaitanya', 'Vardhan', 'Python', 'Anaconda']
    new_string = transform_string(input_string, targets, surround_with('*'))
    print(new_string)
