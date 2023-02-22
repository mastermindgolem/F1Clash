import pymongo, csv, json

client = pymongo.MongoClient("mongodb+srv://golem:OHPwJCrwdufNxsWE@f1clash.cuqr1gk.mongodb.net/?retryWrites=true&w=majority")
d = client.F1Clash
db = d.tracks
data = []
tracks = json.loads(open("TrackInfo.json").read())
for track in tracks:
    data.append(tracks[track])
db.insert_many(data)
