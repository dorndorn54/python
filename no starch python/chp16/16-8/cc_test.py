import unittest
from country_codes import get_country_code

class CountryTestCase(unittest.TestCase):
    # test for get_country_code function

    def test_get_country_code(self):
        double_cc = get_country_code('Andorra')
        self.assertEqual(double_cc, 'ad')

unittest.main()