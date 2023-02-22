import random
from pprint import pprint
from matplotlib import pyplot as plt
from read_csv import read_csv

N = 100000




data = read_csv("S12_Standard.csv")

def simulate(assets:dict,total_min:int,total_max:int):
    #variable to decide when simulation passes all conditions
    satisfied = False
    
    min_assets = min([asset["Min"] for asset in assets.values()])
    max_assets = max([asset["Max"] for asset in assets.values()])
    result = []
    if sum([asset["Drop_Rate"] for asset in assets.values()]) < random.random()*100:
        satisfied = True
        return result
    while not satisfied:
        satisfied = True
        crateSetCombo = findCrateSetCombo(min_assets, max_assets, total_min, total_max)
        chosenDrivers = random.choices(population=[asset for asset in assets], weights=[asset["Drop_Rate"] for asset in assets.values()], k=len(crateSetCombo))
        for i in range(len(chosenDrivers)):
            if crateSetCombo[i] > assets[chosenDrivers[i]]["Max"] or crateSetCombo[i] < assets[chosenDrivers[i]]["Min"]:
                satisfied = False
            result.append([chosenDrivers[i], crateSetCombo[i]])
        if not satisfied:
            result = []
    return result

def findCrateSetCombo(min_assets, max_assets, min_total, max_total):
    if min_assets == 0:
        min_assets = 1
    total = []
    while sum(total) < min_total or sum(total) > max_total:
        total.append(random.randint(min_assets,max_assets))
        
        if sum(total) > max_total:
            total = []
    return total

results = {}


for i in range(N):
    print(i+1)
    total_assets = 5
    while total_assets > 4:
        common = len(simulate({k:v for k,v in data.items() if "Common" in k}, 37, 39))
        rare = len(simulate({k:v for k,v in data.items() if "Rare" in k}, 5, 6))
        epic = len(simulate({k:v for k,v in data.items() if "Epic" in k}, 1,1))
        total_assets = common+rare+epic
    r = f"{common}C-{rare}R-{epic}E"
    if r not in results:
        results[r] = 0
    results[r] += 1

pprint(results)

plt.bar(results.keys(), results.values())
plt.xticks(rotation=90)
plt.show()
