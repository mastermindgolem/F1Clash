import csv
import math
import statistics

data = []
with open("Simulations/S12_Standard.csv") as f:
    csvreader = csv.reader(f)
    headers = next(csvreader)
    for row in csvreader:
        if row[1] == "C" or row[1] == "Common":
        #if row[1] == "R" or row[1] == "Rare":
        #if row[1] == "E" or row[1] == "Epic":
            data.append(float(row[2]))

print(sum(data))
print(len(data))
print(statistics.mean(data))
print(statistics.stdev(data))
print(statistics.median(data))