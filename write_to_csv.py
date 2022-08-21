import csv

data = "5M3M 5H3S 5M3M 5H3S 4M4M 5H3S 4S4H 3S5H 3S5H 3S5H 4M4H 5H3S 3S5H 3S5H 4M4H 3S5H 4M4H 3S5H 4M4H 4M4H"
track = "Barcelona"
rows = []

data = data.split()

for i in range(len(data)):
    temp = data[i]
    if len(temp) == 4:
        rows.append([track, i+1,temp[1], temp[0], temp[3], temp[2], "", "", "",1])
    if len(temp) == 6:
        rows.append([track, i+1,temp[1], temp[0], temp[3], temp[2], int(temp[0])+int(temp[2]), temp[5], temp[4],2])

with open("champdata.csv","a") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(rows)
