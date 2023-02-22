import csv

def read_csv(filename):
    data = {}
    with open(filename, newline='') as csvfile:
    
        # Create a CSV reader object
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        # Read the header row
        headers = next(reader)
        
        # Print the header row
        
        # Loop through the remaining rows
        for row in reader:
            new_row = {}
            key = row[0]
            if row[1] == "C":
                key = ("Common_") + key
            elif row[1] == "R":
                key = ("Rare_") + key
            elif row[1] == "E":
                key = ("Epic_") + key
            else:
                key = row[1] + ("_") + key
            
            new_row["Drop_Rate"] = float(row[2])
            new_row["Min"] = int(row[3])
            new_row["Max"] = int(row[4])
            data[key] = new_row
    return data