from pprint import pprint
boosts = {}
for line in open('temp.txt').read().split('\n'):
    if "Tsunoda" in line or "Stroll" in line:
        boost = line.split()[-1]
        if boost not in boosts:
            boosts[boost] = 0
        boosts[boost] += line.count('-')

pprint(boosts)