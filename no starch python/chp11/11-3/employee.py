class Employee():
    # a class for employees take first name last name and annual salary
    def __init__(self, first_name, last_name, annual_salary):
        self.first_name = first_name
        self.last_name = last_name
        self.annual_salary = annual_salary

    def give_raise(self, amount = 5000):
        #if not amount is given then it would be 5000 auto
        self.annual_salary += amount