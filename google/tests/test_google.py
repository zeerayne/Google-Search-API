import unittest
import nose
from google import google
from google import currency, images
from mock import Mock
import os


def load_html_file(file_name):

    dir_path = os.path.join(os.path.dirname(__file__), "html_files")
    # file_name = func.__name__ + ".html"
    file_path = os.path.join(dir_path, file_name)

    f = open(file_path, "r")

    return f


class GoogleTest(unittest.TestCase):

    # @unittest.skip("skip")
    # @load_html_file
    def test_search_images(self):
        """Test method to search images."""

        # replace method to get html from a test html file
        f = load_html_file("test_search_images.html")
        google.images.get_html_from_dynamic_site = \
            Mock(return_value=f.read().decode('utf8'))

        res = google.search_images("apple", num_images=10)
        self.assertEqual(len(res), 10)

    # @unittest.skip("skip")
    def test_calculate(self):
        """Test method to calculate in google."""

        # replace method to get html from a test html file
        f = load_html_file("test_calculator.html")
        google.calculator.get_html_from_dynamic_site = \
            Mock(return_value=f.read().decode('utf8'))

        calc = google.calculate("157.3kg in grams")
        self.assertEqual(calc.value, 157300)

    # @unittest.skip("skip")
    def test_exchange_rate(self):
        """Test method to get an exchange rate in google."""

        # replace method to get html from a test html file
        f = load_html_file('test_exchange_rate.html')
        google.currency.get_html = \
            Mock(return_value=f.read().decode('utf8'))

        usd_to_eur = google.exchange_rate("USD", "EUR")
        self.assertGreater(usd_to_eur, 0.0)

    # @unittest.skip("skip")
    def test_convert_currency(self):
        """Test method to convert currency in google."""

        # replace method to get html from a test html file
        f = load_html_file('test_convert_currency.html')
        google.currency.get_html = \
            Mock(return_value=f.read().decode('utf8'))

        euros = google.convert_currency(5.0, "USD", "EUR")
        self.assertGreater(euros, 0.0)

    def test_search(self):
        """Test method to search in google."""

        # replace method to get html from a test html file
        f = load_html_file('test_standard_search.html',)
        google.standard_search.get_html = \
            Mock(return_value=f.read().decode('utf8'))

        search = google.search("github")
        self.assertNotEqual(len(search), 0)

    def test_shopping(self):
        """Test method for google shopping."""

        # replace method to get html from a test html file
        f = load_html_file('test_shopping_search.html')
        google.shopping_search.get_html = \
            Mock(return_value=f.read().decode('utf8'))

        shop = google.shopping("Disgaea 4")
        self.assertNotEqual(len(shop), 0)

# @unittest.skip("skip")


class ConvertCurrencyTest(unittest.TestCase):

    # @unittest.skip("skip")
    def test_get_currency_req_url(self):
        """Test method to get currency conversion request url."""

        amount = 10
        from_currency = "USD"
        to_currency = "EUR"
        req_url = currency._get_currency_req_url(amount, from_currency,
                                                 to_currency)

        exp_req_url = "https://www.google.com/finance/converter?a=10&from=USD&to=EUR"

        self.assertEqual(req_url, exp_req_url)

    # @unittest.skip("skip")
    def test_parse_currency_response(self):
        """Test method to parse currency response. TODO!"""
        pass

# @unittest.skip("skip")


class SearchImagesTest(unittest.TestCase):

    def test_get_images_req_url(self):

        query = "banana"
        options = images.ImageOptions()
        options.image_type = images.ImageType.CLIPART
        options.larger_than = images.LargerThan.MP_4
        options.color = "green"

        req_url = images._get_images_req_url(query, options)

        exp_req_url = 'https://www.google.com.ar/search?q=banana&es_sm=122&source=lnms&tbm=isch&sa=X&ei=DDdUVL-fE4SpNq-ngPgK&ved=0CAgQ_AUoAQ&biw=1024&bih=719&dpr=1.25&tbs=itp:clipart,isz:lt,islt:4mp,ic:specific,isc:green'

        self.assertEqual(req_url, exp_req_url)


if __name__ == '__main__':
    # nose.main()
    nose.run(defaultTest=__name__)
