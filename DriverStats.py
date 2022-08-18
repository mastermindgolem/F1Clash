import csv


def fetchDriverStats(driverName, driverRarity, driverLevel):
    driverStats = open("DriverStats.csv")

    data = csv.reader(driverStats)
    headers = next(data)

    driverStats = {}
    for row in data:
        driverStats[row[0]] = {}
        for i in range(1,len(row)):
            driverStats[row[0]][headers[i]] = row[i]

    print(driverStats[driverName + driverRarity + str(driverLevel)])