from functools import wraps

def currency(f):
    """return a function by uses the passed funciton"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        return '{} {}'.format('$', f(*args, **kwargs))

    return wrapper

class Product():
    def __init__(self, price, tax):
        self.price = price
        self.tax = tax

    @currency
    def price_with_tax(self):
        return self.price * (1 + self.tax * .01)

if __name__ == '__main__':
    product = Product(29.99, 10.0)
    print(product.price_with_tax())
    print('__name__:{} __doc__:{}'.format(product.price_with_tax.__name__, product.price_with_tax.__doc__))
