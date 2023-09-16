# take two numbers and then add together
# convert to int and if not int produce type error

def add_numbers(num1, num2):
    try:
        #add the two numbers together
        sum = int(num1) + int(num2)
        print(sum)
    except ValueError:
        print("one of the numbers are not integers")
        

def get_numbers():
    print("This program adds two numbers together")
    num1 = input("what is the first number: ")
    num2 = input("what is the second number: ")
    add_numbers(num1, num2)

get_numbers()