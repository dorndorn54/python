from random import randint

class Die():
    # a class represnting a single die
    def __init__(self, num_sides=6):
        # assume a 6 sided die
       self.num_sides = num_sides

    def roll(self):
        # return a random value from 1 to 6
        return randint(1, self.num_sides)
