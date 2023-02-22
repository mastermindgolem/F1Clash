import pymongo, csv

client = pymongo.MongoClient("mongodb+srv://golem:OHPwJCrwdufNxsWE@f1clash.cuqr1gk.mongodb.net/?retryWrites=true&w=majority")
d = client.F1Clash
db = d.components
db.delete_many({})
data = []
"Name,Rarity,Level,Power,Aero,Grip,Reliability,Pit Time,Total,Series,Cards For Upgrade,Total Cards Needed,Coins For Upgrade,Total Coins Needed"
with open("componentstats.csv") as f:
    csvreader = csv.reader(f)
    headers = next(csvreader)
    for row in csvreader:
        data.append({
            "Name": row[0],
            "Rarity": row[1],
            "Level": int(row[2]),
            "Power": int(row[3]),
            "Aero": int(row[4]),
            "Grip": int(row[5]),
            "Reliability": int(row[6]),
            "Pit Time": float(row[7]),
            "Multiplier": 1,
            "Series": int(row[9]),
            "Cards For Upgrade": int(row[10]),
            "Total Cards Needed": int(row[11]),
            "Coins For Upgrade": int(row[12]),
            "Total Coins Needed": int(row[13])
        })
db.insert_many(data)
