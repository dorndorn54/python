people = [] # empty list to store

person_1 = {'first_name' : 'John', 'surname' : 'Lee', 'age' : '27'}
people.append(person_1)
person_2 = {'first_name' : 'Tim', 'surname' : 'tan', 'age' : '29'}
people.append(person_2)
person_3 = {'first_name' : 'cook', 'surname' : 'kim', 'age' : '45'}
people.append(person_3)

for person in people:
    name = str(person['first_name'].title()) + " " + str(person['surname'].title())
    age = str(person['age'])

    print(name + ' is ' + age)
