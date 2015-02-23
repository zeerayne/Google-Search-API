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
