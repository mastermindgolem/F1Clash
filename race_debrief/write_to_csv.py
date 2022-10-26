import csv


def write_race_debrief(series, track, data):
    gp = ''
    rows = []
    try:
        if int(series) > 0:
            series = series
        else:
            series = '-'
            gp = series
    except Exception:
        series = '-'
        gp = series
    data = data.split()
    print(data)
    print(len(data))
    for i in range(len(data)):
        temp = data[i]
        if len(temp) == 4:
            l = [track, series, i+1,temp[1], temp[0], temp[3], temp[2], "", "", "",1,"", temp[1]]
            for i in range(1,int(temp[0])):
                l.append(temp[1] + " RACE")
            l.append(temp[3])
            for i in range(1,int(temp[2])):
                l.append(temp[3] + " RACE")
            while len(l) < 21:
                l.append('-')
            if gp != '':
                l.append(gp)
            rows.append(l)
        if len(temp) == 6:
            l = [track, series, i+1,temp[1], temp[0], temp[3], temp[2], int(temp[0])+int(temp[2]), temp[5], temp[4],2, "", temp[1]]
            for i in range(1,int(temp[0])):
                l.append(temp[1] + " RACE")
            l.append(temp[3])
            for i in range(1,int(temp[2])):
                l.append(temp[3] + " RACE")
            l.append(temp[5])
            for i in range(1,int(temp[4])):
                l.append(temp[5] + " RACE")
            while len(l) < 21:
                l.append('-')
            if gp != '':
                l.append(gp)
            rows.append(l)
    msg = ""
    if len(rows) != 20:
        return f"Error! not 20 entries\n{data}"
    for row in rows:
        for col in row:
            msg = msg + str(col) + ","
        msg = msg[:-1] + "\n"    
    return msg
