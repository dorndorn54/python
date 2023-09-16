import unittest
from city_function import city_functions

class CityTestCase(unittest.TestCase):
    # test for city_function.py

    def test_city(self):
        #do the two inputs work
        test_city_functions = city_functions('singapore', 'singapore', 5000)
        self.assertEqual(test_city_functions, 'singapore, singapore population - 5000')

unittest.main()