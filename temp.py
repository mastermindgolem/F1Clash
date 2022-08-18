import math

#S 3-4 28.889
#M 3-5 29.976
#H 4-6 31.777

#Total Laps
laps = 8
#1 Pit Strat
pitstop1 = True
#2 Pit Strat
pitstop2 = True
#Laps to not pit on
ignore_laps = []

#Tyre data from pre-race screen
tyres = {
    "Soft": {
        "min": 3,
        "max": 4,
        "time": 28.762
    },
    "Medium": {
        "min": 3,
        "max": 5,
        "time": 30.024
    },
    "Hard": {
        "min": 4,
        "max": 7,
        "time": 31.820
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
                lap_options.append([t, i, "RED", tyres[t]['time']/1.1*i, 1.5*i, 0.25*i])
            else:
                lap_options.append([t, i, "YELLOW", tyres[t]['time']*i, 1*i, 0.17*i])
    for a in lap_options:
        print(a)
    return lap_options

def simulateRace():
    lap_options = tyre_selection()
    pit1_options = []
    pit2_options = []
    for a in range(1,laps):
        for b in range(1,laps):
            if a + b == laps:
                pit1_options.append([a,b])
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
                    if option_a[4] + option_b[4] + option_c[4] < 9:
                        fuel = 9 - option_a[4] - option_b[4] - option_c[4]
                        service = 1 - option_a[5] - option_b[5] - option_c[5]
                        totaltime = option_a[3] + option_b[3] + option_c[3]
                        if option_a[1] in ignore_laps or option_a + option_b in ignore_laps:
                            continue
                        if option_a[5] + option_b[5] > 1:
                            service += 1
                            final_options.append([totaltime+2, fuel, service, option_a[:3], "SERVICE", option_b[:3], "PIT", option_c[:3]])
                        elif option_a[5] + option_b[5] + option_c[5] > 1:
                            service += 1
                            final_options.append([totaltime+2, fuel, service, option_a[:3], "PIT", option_b[:3], "SERVICE", option_c[:3]])
                        else:
                            final_options.append([totaltime, fuel, service, option_a[:3], "PIT", option_b[:3], "PIT", option_c[:3]])
          
    for option in pit1_options:
        for option_a in list(filter(lambda x:x[1] == option[0], lap_options)):
            for option_b in list(filter(lambda x:x[1] == option[1], lap_options)):
                if option_a[4] + option_b[4] < 9:
                    fuel = 9 - option_a[4] - option_b[4]
                    service = 1 - option_a[5] - option_b[5]
                    totaltime = option_a[3] + option_b[3]
                    if option_a[1] in ignore_laps:
                        continue
                    if option_a[5] + option_b[5] > 1:
                        service += 1
                        final_options.append([totaltime+2, fuel, service, option_a[:3], "SERVICE", option_b[:3]])
                    else:
                        final_options.append([totaltime, fuel, service, option_a[:3], "PIT", option_b[:3]])
    final_options.sort(key = lambda x:x[0])
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