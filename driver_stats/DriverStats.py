import csv
from math import floor

def fetchDriverStats(driverName, driverRarity, driverLevel, boostedDrivers, boostedComps):
    driverStats = open("driver_stats/DriverStats.csv")

    data = csv.reader(driverStats)
    headers = next(data)

    driverStats = {}
    stats = ["Overtaking", "Defending", "Consistency", "Fuel Use", "Tyre Mgmt", "Wet Ability", "Total Value", "Dry Quali"]
    for row in data:
        if row[1] in boostedDrivers:
            multiplier = 1.1
        else:
            multiplier = 1
        driverStats[row[0]] = {}
        for i in range(1,len(row)):
            try:
                if headers[i] in stats:
                    driverStats[row[0]][headers[i]] = str(floor(int(row[i])*multiplier))
                else:
                    driverStats[row[0]][headers[i]] = str(floor(int(row[i])))
            except Exception:
                driverStats[row[0]][headers[i]] = row[i]

    return(driverStats[driverName + driverRarity + str(driverLevel)])