import csv

from matplotlib import pyplot as plt

# get the temp data from the file
filename = "sitka_weather_07-2018_simple.csv"
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    
    # high data
    highs = []
    for row in reader:
        highs.append(row[5])

print(highs)


