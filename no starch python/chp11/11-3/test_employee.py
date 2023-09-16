import unittest
from employee import Employee

class TestEmployee(unittest.TestCase):
    # a class to test the Employee class
    def setUp(self):
        # make an employee
        self.eric = Employee('john', 'tan', 65000)

    def test_give_default_raise(self):
        # to test if the default raise works properly
        self.eric.give_raise() #empty
        self.assertEqual(self.eric.annual_salary, 70000)

    def test_alt_raise(self):
        # test if the alternative raise works properly
        self.eric.give_raise(7000)
        self.assertEqual(self.eric.annual_salary, 72000)

unittest.main()