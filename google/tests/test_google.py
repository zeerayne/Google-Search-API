import unittest
import nose
from google import google
from mock import Mock


class GoogleTest(unittest.TestCase):

    def setUp(self):

        # replace method to get html with a test html file
        f = open('test_search_images.html', 'r')
        google.images.get_html_from_dynamic_site = \
            Mock(return_value=f.read().decode('utf8'))

    def test_search_images(self):
        """Test method to search images."""

        res = google.Google.search_images("apple", num_images=10)
        self.assertEqual(len(res), 10)

    @unittest.skip("skip")
    def test_exchange_rate(self):
        """Test method to get an exchange rate in google."""

        usd_to_eur = google.Google.convert_currency("USD", "EUR")
        self.assertGreater(usd_to_eur, 0.0)

    # @unittest.skip("skip")
    def test_convert_currency(self):
        """Test method to convert currency in google."""

        euros = google.Google.convert_currency(5.0, "USD", "EUR")
        self.assertGreater(euros, 0.0)

    @unittest.skip("skip")
    def test_calculate(self):
        """Test method to calculate in google."""

        calc = google.Google.calculate("157.3kg in grams")
        self.assertEqual(calc.value, 157300)

    def test_search(self):
        """Test method to search in google."""

        search = google.Google.search("github")
        self.assertNotEqual(len(search), 0)

    def test_shopping(self):
        """Test method for google shopping."""

        shop = google.Google.shopping("Disgaea 4")
        self.assertNotEqual(len(shop), 0)


class ConvertCurrencyTest(unittest.TestCase):

    # @unittest.skip("skip")
    def test_get_currency_req_url(self):
        """Test method to get currency conversion request url."""

        amount = 10
        from_currency = "USD"
        to_currency = "EUR"
        req_url = google.Google._get_currency_req_url(amount, from_currency,
                                                      to_currency)

        expected_req_url = "https://www.google.com/finance/converter?a=10&from=USD&to=EUR"

        self.assertEqual(req_url, expected_req_url)


if __name__ == '__main__':
    nose.main()
