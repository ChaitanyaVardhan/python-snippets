def is_even(number):
    """checks whether the number is even"""
    return (number % 2) == 0

def count_occurences(input_list, predicate):
    """returns the number of times applying predicate to
    a list element returns true"""
    return sum([1 for e in input_list if predicate(e)])

if __name__ == '__main__':
    my_predicate = is_even
    my_list = [1,2,3,4,5,6,7,8,9,10]
    result = count_occurences(my_list, my_predicate)
    print result
