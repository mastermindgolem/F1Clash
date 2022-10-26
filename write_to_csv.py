import csv

data = "3S3S1S 4M3H 4M3H 3S4M 4H3M 4M3H 4H3M 4H3M 3M4H 4H3H 4H3H 4H3M 3M4H 3S3S1S 3M4H 2S3M2M 2S2S3M 4H3H 4H3H"
track = "Suzuka"
rows = []

data = data.split()

for i in range(len(data)):
    temp = data[i]
    if len(temp) == 4:
        rows.append([track, i+1,temp[1], temp[0], temp[3], temp[2], "", "", "",1])
    if len(temp) == 6:
        rows.append([track, i+1,temp[1], temp[0], temp[3], temp[2], int(temp[0])+int(temp[2]), temp[5], temp[4],2])

with open("champdata.csv","w") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(rows)
