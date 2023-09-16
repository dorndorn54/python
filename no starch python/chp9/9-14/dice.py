from random import randint

class Die():
    #represent a 6 sided Die
    def __init__(self, sides = 6):
        self.sides = sides

    def roll_die(self):
        #method to roll die and print out the value
        return randint(1, self.sides)

results = []
d6 = Die()
for roll in range(10):
    result = d6.roll_die()
    results.append(result)
print("the results of the die are", end="")
print(results)

d10 = Die(10)
results_2 = []
for roll in range(10):
    result_2 = d10.roll_die()
    results_2.append(result_2)
print("the results of the die are", end="")
print(results_2)
