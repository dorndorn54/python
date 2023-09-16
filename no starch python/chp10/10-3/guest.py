filename = 'guest.txt'

while True:
    user_input = input("what is your name: ")

    if user_input == '':
        print("Thank you.")
        break

    with open(filename, 'a') as file_object:
        file_object.write(user_input + "\n")

