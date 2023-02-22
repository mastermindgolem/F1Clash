from pprint import pprint



data = "2M2S3H1S 3H3H2M 3H3H2M 2H2S2S2H 3H2S2S1S 3H2S2S1S 3H2S3H 2S3H3H 2S2S2M2M 2S2S2M2M 3H3H2H 2M3H3M 3H3H2S 3H2S3H 2M2S2S2S 2S2S2M2M 2M2H2S2M 2S3H3H 2S2S2S2H 2M2S3H1S"
#track = "Miami"
#series = "7"
track = "Jeddah"
#series = "10"
series = "12"


rows = []
drivers = data.split(" ")
for i in range(len(drivers)):
    row = []
    row.append(track)
    row.append(series)
    row.append(str(i+1))
    a = []
    for j in range(0,7,2):
        try:
            row.append((drivers[i][j]))
            a.append(drivers[i][j+1])
            for k in range(int(drivers[i][j])-1):
                a.append(drivers[i][j+1] + "R")
        except:
            row.append("")
    row.extend(a)
    rows.append(",".join(row))


with open("data.csv",'a') as f:
    f.write("\n".join(rows) + "\n")