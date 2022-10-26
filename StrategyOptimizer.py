import math
from DriverStats import fetchDriverStats
import json

#Track Name
track = "Austin"
track_data = json.loads(open("TrackInfo.json").read())[track]


#Total Laps
laps = track_data['laps']
starting_fuel = laps + 1.83
#1 Pit Strat
pitstop1 = True
#2 Pit Strat
pitstop2 = True
#Laps to not pit on
ignore_laps = [4]
#Time lost by pitting
pit_time = track_data['extra_pit_time'] + 3.55

#Tyre data from pre-race screen
tyres = {
    "Soft": {
        "min": 3,
        "max": 4,
        "time": 31.916
    },
    "Medium": {
        "min": 3,
        "max": 4,
        "time": 32.930
    },
    "Hard": {
        "min": 3,
        "max": 5,
        "time": 34.144
    }
}


#Add all different stint options
def tyre_selection():
    lap_options = []
    for t in tyres:
        for i in range(1,tyres[t]['max']+1):
            #Format - TyreType, No. of laps, Mode, Time for all laps, Fuel for all laps, Service for all laps
            if i == tyres[t]['max']:
                lap_options.append([t, i, "GREEN", tyres[t]['time']*1.1*i, 0.67*i, 0.08*i])
            elif i <= tyres[t]['min']:
                lap_options.append([t, i, "RED", tyres[t]['time']*0.9*i, 1.5*i, 0.25*i])
            else:
                lap_options.append([t, i, "YELLOW", tyres[t]['time']*i, 1*i, 0.17*i])
    for a in lap_options:
        print(a)
    return lap_options

def simulateRace():
    lap_options = tyre_selection()
    pit1_options = []
    pit2_options = []
    #Find all 1 pit options
    for a in range(1,laps):
        for b in range(1,laps):
            if a + b == laps:
                pit1_options.append([a,b])
    #Find all 2 pit options
    for a in range(1,laps):
        for b in range(1,laps):
            for c in range(1,laps):
                if a+b+c == laps:
                    pit2_options.append([a,b,c])
    if not pitstop1:
        pit1_options = []
    if not pitstop2:
        pit2_options = []
    final_options = []
    for option in pit2_options:
        for option_a in list(filter(lambda x:x[1] == option[0], lap_options)):
            for option_b in list(filter(lambda x:x[1] == option[1], lap_options)):
                for option_c in list(filter(lambda x:x[1] == option[2], lap_options)):
                    #Check if more than available fuel needed
                    if option_a[4] + option_b[4] + option_c[4] < starting_fuel:
                        #Find final used
                        fuel = option_a[4] + option_b[4] + option_c[4]
                        #Find service used
                        service = option_a[5] + option_b[5] + option_c[5]
                        #Find total race time
                        totaltime = option_a[3] + option_b[3] + option_c[3] + pit_time*2
                        #Don't continue if pitting lap will result in traffic
                        if option_a[1] in ignore_laps or option_a[1] + option_b[1] in ignore_laps:
                            continue
                        #Check if you must service on first pit
                        if option_a[5] + option_b[5] > 1:
                            final_options.append([totaltime+2, fuel, service, option_a[:3], "SERVICE", option_b[:3], "PIT", option_c[:3]])
                        #Check if you must service on second pit
                        elif option_a[5] + option_b[5] + option_c[5] > 1:
                            final_options.append([totaltime+2, fuel, service, option_a[:3], "PIT", option_b[:3], "SERVICE", option_c[:3]])
                        else:
                            final_options.append([totaltime, fuel, service, option_a[:3], "PIT", option_b[:3], "PIT", option_c[:3]])
          
    for option in pit1_options:
        for option_a in list(filter(lambda x:x[1] == option[0], lap_options)):
            for option_b in list(filter(lambda x:x[1] == option[1], lap_options)):
                #Check if more than available fuel needed
                if option_a[4] + option_b[4] < starting_fuel:
                    #Find fuel used
                    fuel = option_a[4] + option_b[4]
                    #Find service used
                    service = option_a[5] + option_b[5]
                    #Find total race time
                    totaltime = option_a[3] + option_b[3] + pit_time
                    #Don't continue if pitting lap results in traffic
                    if option_a[1] in ignore_laps:
                        continue
                    #Check if service needed on pit
                    if option_a[5] + option_b[5] > 1:
                        final_options.append([totaltime+2, fuel, service, option_a[:3], "SERVICE", option_b[:3]])
                    else:
                        final_options.append([totaltime, fuel, service, option_a[:3], "PIT", option_b[:3]])
    #Sort by smallest race time
    final_options.sort(key = lambda x:x[0])
    #Print headers
    print("\tTime\tFuel\tService\t|Tyres\tLaps\tMode\tStint 1\t|Tyres\tLaps\tMode\tStint 2\t|Tyres\tLaps\tMode\tStint 3")
    for i in range(len(final_options)):
        a = final_options[i]
        a[0] = round(a[0],2)
        a[1] = round(a[1],3)
        a[2] = round(a[2],3)
        print(i+1, end = '\t')
        for b in a:
            if type(b) == list:
                print("|", end = '')
                for c in b:
                    print(c, end = '\t')
            else:
                print(b, end = '\t')
        print('')

simulateRace()