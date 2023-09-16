filename = 'learning_python.txt'

with open(filename) as file_object:
    lines = file_object.readlines() #store it in a list 1 line 1 item in list

for line in lines:
    print(line.rstrip())