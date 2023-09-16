while True:
    print("This program adds two numbers together")
    num1 = input("what is the first number: ")
    num2 = input("what is the second number: ")

    try:
        sum = int(num1) + int(num2)
        print(sum)
        break
    except ValueError:
        print("one of the numbers are not integers")