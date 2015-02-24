import unittest
import nose
from google import currency


class ConvertCurrencyTest(unittest.TestCase):

    def test_convert(self):
        """Test method to convert currency in currency module."""

        euros = currency.convert(5.0, "USD", "EUR")
        self.assertGreater(euros, 0.0)

    # @unittest.skip("skip")
    def test_exchange_rate(self):
        """Test method to get an exchange rate in currency module."""

        usd_to_eur = currency.exchange_rate("USD", "EUR")
        self.assertGreater(usd_to_eur, 0.0)

    # @unittest.skip("skip")
    def test_get_currency_req_url(self):
        """Test method to get currency conversion request url."""

        amount = 10
        from_currency = "USD"
        to_currency = "EUR"
        req_url = currency._get_currency_req_url(amount, from_currency,
                                                 to_currency)

        expected_req_url = "https://www.google.com/finance/converter?a=10&from=USD&to=EUR"

        self.assertEqual(req_url, expected_req_url)

    @unittest.skip("skip")
    def test_parse_currency_response(self):
        """Test method to parse currency response. TODO!"""
        pass


if __name__ == '__main__':
    # nose.main()
    nose.run(defaultTest=__name__)
