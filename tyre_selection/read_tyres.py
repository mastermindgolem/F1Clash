data = """Golden Grand Slam
I LE CASTELLET
Weather Forecast
17°c
18°
16°c
SELECT A TYRE COMPOUND TO START THE RACE WITH
13
P. Gasly
G. Russell
(S) SOFT
GRIP
HIGH
LAPS
2-3
00.36:293
(M) MEDIUM
GRIP
MEDIUM
LAPS
3-4
00.37:267
+ HARD
GRIP
LOW
LAPS
3.5
00.38:980
W WET
GRIP
WET
LAPS
3-4
00.44:596
S) SOFT
GRIP
HIGH
LAPS
2.3
00.36:297
(M) MEDIUM
GRIP
MEDIUM
LAPS
3°4
00.36:696
(H) HARD
GRIP
LAPS
LOW
3.5
00.38:384
W WET
GRIP
WET
LAPS
3-4
00.43:959"""

temp = []
for line in data.split("\n"):
    if ":" in line and "." in line:
        temp.append(line[3:].replace(":","."))
    if ";" in line and "." in line:
        temp.append(line[3:].replace(";","."))
        
print(temp[0] + '\n' + temp[4] + '\n' + temp[1] + '\n' + temp[5] + '\n' + temp[2] + '\n' + temp[6] + '\n' + temp[3] + '\n' + temp[7])