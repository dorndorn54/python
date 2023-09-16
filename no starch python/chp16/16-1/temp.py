import csv

# get the temp data from the file
filename = "sitka_weather_07-2018_simple.csv"
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

highs = []
for row in reader:
    highs.append(row[5])
 
print(highs)