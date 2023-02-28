import pymongo, csv, json

client = pymongo.MongoClient("mongodb+srv://golem:OHPwJCrwdufNxsWE@f1clash.cuqr1gk.mongodb.net/?retryWrites=true&w=majority")
d = client.F1Clash
db = d.strategies
data = [
    {
        "Track Name": "Bahrain",
        "Characteristics": [],
        "Overtaking Zones": [],
        "Track Image": "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Bahrain_Circuit.png.transform/7col-retina/image.png",
        "Dry": {"Front":[], "Mid":[], "Back":[]},
        "Wet": {"Front":[], "Mid":[], "Back":[]}
    },
    {
        "Track Name": "Abu Dhabi",
        "Characteristics": [],
        "Overtaking Zones": [],
        "Track Image": "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Abu_Dhabi_Circuit.png.transform/7col-retina/image.png",
        "Dry": {"Front":[], "Mid":[], "Back":[]},
        "Wet": {"Front":[], "Mid":[], "Back":[]}
    },
    {
        "Track Name": "Miami",
        "Characteristics": [],
        "Overtaking Zones": [],
        "Track Image": "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Miami_Circuit.png.transform/7col-retina/image.png",
        "Dry": {"Front":[], "Mid":[], "Back":[]},
        "Wet": {"Front":[], "Mid":[], "Back":[]}
    },
    {
        "Track Name": "Jeddah",
        "Characteristics": [],
        "Overtaking Zones": [],
        "Track Image": "https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Saudi_Arabia_Circuit.png.transform/7col-retina/image.png",
        "Dry": {"Front":[], "Mid":[], "Back":[]},
        "Wet": {"Front":[], "Mid":[], "Back":[]}
    }
]
db.insert_many(data)
