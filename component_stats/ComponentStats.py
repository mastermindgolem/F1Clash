import csv


def fetchCompStats(compName, level, boostedDrivers, boostedComps):
    componentStats = open("component_stats/ComponentData.csv")

    data = csv.reader(componentStats)
    headers = next(data)

    compStats = {}
    for row in data:
        if row[1] not in compStats:
            compStats[row[1]] = {}
        if row[2] not in compStats[row[1]]:
            compStats[row[1]][row[2]] = {}
        if any([d in row[0] for d in boostedComps]):
            multiplier = 1.1
        else:
            multiplier = 1
        
        for i in range(3,len(row)):
            try:
                compStats[row[1]][row[2]][headers[i]] = float(row[i])*multiplier
            except Exception:
                compStats[row[1]][row[2]][headers[i]] = row[i]
        compStats[row[1]][row[2]]["Team Score"] = compStats[row[1]][row[2]]["Power"] + compStats[row[1]][row[2]]["Aero"] + compStats[row[1]][row[2]]["Grip"] + compStats[row[1]][row[2]]["Reliability"] + (1-compStats[row[1]][row[2]]["Pit Time"])*46

            
    return(compStats[compName][str(level)])