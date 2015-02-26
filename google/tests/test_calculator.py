import unittest
import nose
from google import calculator
from mock import Mock


class CalculatorTest(unittest.TestCase):

    def test_calculate(self):
        """Test method to use google as a calculator."""

        # replace method to get html with a test html file
        f = open('test_calculator.html', 'r')
        calculator.get_html_from_dynamic_site = \
            Mock(return_value=f.read().decode('utf8'))

        calc = calculator.calculate("157.3kg in grams")
        self.assertEqual(calc.value, 157300)


if __name__ == '__main__':
    # nose.main()
    nose.run(defaultTest=__name__)
