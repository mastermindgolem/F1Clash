from pprint import pprint
import json, pymongo
client = pymongo.MongoClient("mongodb+srv://golem:OHPwJCrwdufNxsWE@f1clash.cuqr1gk.mongodb.net/?retryWrites=true&w=majority")
d = client.F1Clash
db = d.strategies

data = open("Strategies/s.txt").read().split("\n")
j = {}
j['Track Name'] = data[0]
j['Characteristics'] = data[1].split("/")
j['Overtaking Zones'] = list([int(i) for i in data[2].split("/")])
j['Track Image'] = data[3]
j['Dry'] = {
    "Front": [{"strategy1": data[4].replace("-"," | "), "boost1": data[5], "strategy2": data[6].replace("-"," | "), "boost2": data[7]}],
    "Mid": [{"strategy1": data[8].replace("-"," | "), "boost1": data[9], "strategy2": data[10].replace("-"," | "), "boost2": data[11]}],
    "Back": [{"strategy1": data[12].replace("-"," | "), "boost1": data[13], "strategy2": data[14].replace("-"," | "), "boost2": data[15]}]
}
if len(data) > 16:
    j['Wet'] = {
        "Front": [{"strategy1": data[16].replace("-"," | "), "boost1": data[17], "strategy2": data[18].replace("-"," | "), "boost2": data[19]}],
        "Mid": [{"strategy1": data[20].replace("-"," | "), "boost1": data[21], "strategy2": data[22].replace("-"," | "), "boost2": data[23]}],
        "Back": [{"strategy1": data[24].replace("-"," | "), "boost1": data[25], "strategy2": data[26].replace("-"," | "), "boost2": data[27]}]
    }
db.insert_one(j)