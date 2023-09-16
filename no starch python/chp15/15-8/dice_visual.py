import pygal
from die import Die

# create two D8 dice
die_1 = Die()
die_2 = Die()
die_3 = Die()

# make some rolls, and store results in a list
results = []
for roll_num in range(1000):
    result = die_1.roll() + die_2.roll() + die_3.roll()
    results.append(result)

# analysis of the results
frequencies = []
max_result = die_1.num_sides + die_2.num_sides + die_3.num_sides
for num_value in range(1, max_result + 1):
    frequency = results.count(num_value)
    frequencies.append(frequency)
# generating the histogram
hist = pygal.Bar()
hist.title = "results of rolling three D6 dice 1000 times"
hist.x_labels = list(range(1, max_result + 1))
hist.x_title = "results"
hist.y_title = "freq of result"

hist.add("D6 X 3", frequencies)
hist.render_to_file("dice_visual.svg")
