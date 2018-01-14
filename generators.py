import math

import sys

def get_primes(input_list):
    return [element for element in input_list if is_prime(element)]

#infinitely return prime numbers greater than an input number
def get_primes_gen(number):
    while True:
        if is_prime(number):
            yield number
        number += 1
            
def is_prime(number):
    if number > 1:
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        for divisor in range(3, int(math.sqrt(number) + 1), 2):
            if number % divisor == 0:
                return False
        return True
    return False

def sum_primes_less_than(bound):
    total = 2
    for next_prime in get_primes_gen(3):
        if next_prime < bound:
            total += next_prime
        else:
            print(total)
            return


if __name__ == '__main__':
    bound = int(sys.argv[1])
    print "bound: {}".format(bound)
    sum_primes_less_than(bound)

