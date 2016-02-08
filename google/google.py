from __future__ import unicode_literals

try:
    from modules import images
    from modules import currency
    from modules import calculator
    from modules import standard_search
    from modules import shopping_search
except ImportError:
    from google.modules import images
    from google.modules import currency
    from google.modules import calculator
    from google.modules import standard_search
    from google.modules import shopping_search

__author__ = "Anthony Casagrande <birdapi@gmail.com>, " + \
    "Agustin Benassi <agusbenassi@gmail.com>"
__version__ = "1.1.0"


"""Defines the public inteface of the API."""

search = standard_search.search
search_images = images.search
convert_currency = currency.convert
exchange_rate = currency.exchange_rate
calculate = calculator.calculate
shopping = shopping_search.shopping

if __name__ == "__main__":
    import doctest
    doctest.testmod()
