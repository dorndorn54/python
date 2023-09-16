import json

filename = 'name.txt'

def prompt_user():
    # receive the person name
    number = input("What is your favourite number: ")
    # store name in file
    try:
        with open(filename, 'w') as f_obj:
            json.dump(number, f_obj)
            print('I have saved your favourite number.')
    except FileNotFoundError:
        print('file not found. Please try again')
    else:
        pass

prompt_user()
