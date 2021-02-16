

machine = 0
machines = []

def getM(data, address, Data):
    global machine
    global machines
    data = data.split(".")
    Name = str.join("", data[0:-1])
    if data[-1].upper() in ["XMAX", "XMIN","YMAX","YMIN", "ZMAX", "ZMIN"]:
        if Name not in machines:
            machines.append(Name)
            Data[str(machine)] = {}
            Data[str(machine)]["Name"] = Name
            Data[str(machine)]["Data"] = [[0, 0], [0, 0], [0, 0]]
            machine += 1

        if data[-1].upper() == "XMAX":
            Data[str(len(machines) - 1)]["Data"][0][0] = str(address)
        elif data[-1].upper() == "XMIN":
            Data[str(len(machines) - 1)]["Data"][0][1] = str(address)
        elif data[-1].upper() == "YMAX":
            Data[str(len(machines) - 1)]["Data"][1][0] = str(address)
        elif data[-1].upper() == "YMIN":
            Data[str(len(machines) - 1)]["Data"][1][1] = str(address)
        elif data[-1].upper() == "ZMAX":
            Data[str(len(machines) - 1)]["Data"][2][0] = str(address)
        elif data[-1].upper() == "ZMIN":
            Data[str(len(machines) - 1)]["Data"][2][1] = str(address)





def getData(clipboard=None):
    count = 0
    bcount = 0
    Data = {}
    Data2 = {}
    if clipboard is None:
        with open("data", "r") as f:
            data = f.read()
    else:
        data = clipboard

    for line in data.split("\n"):
        if not len(line) > 0:
            break
        line = line.split("\t")
        if line[1] == "INT":
            # print(count, line[0])
            count += 2
            bcount = 0
        elif line[1] == "REAL":
            getM(line[0], count, Data)
            # print(count , line[0])
            line[0].split(".")
            count += 4
            bcount = 0
        elif line[1] == "BOOL":
            if bcount == 7:
                count += 1
                bcount = 0
            bcount += 1
    return Data








