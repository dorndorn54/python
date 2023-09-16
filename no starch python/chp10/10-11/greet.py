import json

filename = 'name.txt'

def pull_num():
    #obtain number and print it out
    try:
        with open(filename) as f_obj:
            number = json.load(f_obj)
            print('Your favorite number is ' + str(number))
    except FileNotFoundError:
        print('File cannot be found')
    else:
        pass

pull_num()