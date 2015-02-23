import unittest
import nose
from google import google


class GoogleTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @unittest.skip("skip")
    def test_search_images(self):
        """Test method to search images."""

        res = google.Google.search_images("apple", num_images=10)
        self.assertEqual(len(res), 10)

    def test_convert_currency(self):
        pass

    def test_exchange_rate(self):
        pass

    def test_calculate(self):
        pass

    def test_search(self):
        pass

    def test_shopping(self):
        pass


if __name__ == '__main__':
    nose.main()
