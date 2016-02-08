try:
    from modules import calculator, currency, images, utils
    from modules import standard_search, shopping_search
except ImportError:
    from google.modules import calculator, currency, images, utils
    from google.modules import standard_search, shopping_search