#Step 7 Elementary Data Types

Types = {"BOOL":1,"BYTE":8,"WORD":16,"DWORD":32,"INT":16,"DINT":32,"REAL":32,"S5TIME": 16, "TIME":32, "DATE":16, "TIME_OF:DAY" : 32, "CHAR":8}


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

def DataBlock_to_Array(clipboard):
    Types = {"BOOL": 1, "BYTE": 8, "WORD": 16, "DWORD": 32, "INT": 16, "DINT": 32, "REAL": 32, "S5TIME": 16, "TIME": 32,
             "DATE": 16, "TIME_OF:DAY": 32, "CHAR": 8}
    inData = clipboard
    adress = 0
    outData = {}

    for line in inData.split("\n"):
        if not len(line) > 0:
            break
        lineItems = line.split("\t")
        byte = adress // 8
        bit = adress % 8
        adress += Types.get(lineItems[1])
        outData[lineItems[0]] = f"{byte}.{bit}"
    return outData

def Array_to_Struct(Array, masked=None):
    outData = {}
    for key, item in Array.items():
        if "notused" in key.lower(): continue
        if "spare" in key.lower(): continue
        listedName = key.split(".")
        if len(listedName) == 1:

            outData[listedName[0]] = item

        if len(listedName) == 2:
            if listedName[0] not in outData.keys():
                outData[listedName[0]] = {}
            outData[listedName[0]]["".join(listedName[1:])] = item

        if len(listedName) == 3:
            if listedName[0] not in outData.keys():
                outData[listedName[0]] = {}
            if listedName[1] not in outData[listedName[0]].keys():
                outData[listedName[0]][listedName[1]] = {}
            outData[listedName[0]][listedName[1]]["".join(listedName[2:])] = item

        if len(listedName) == 4:
            if listedName[0] not in outData.keys():
                outData[listedName[0]] = {}
            if listedName[1] not in outData[listedName[0]].keys():
                outData[listedName[0]][listedName[1]] = {}
            if listedName[2] not in outData[listedName[0]][listedName[1]].keys():
                outData[listedName[0]][listedName[1]][listedName[2]] = {}
            outData[listedName[0]][listedName[1]][listedName[2]]["".join(listedName[3:])] = item

        if len(listedName) == 5:
            if listedName[0] not in outData.keys():
                outData[listedName[0]] = {}
            if listedName[1] not in outData[listedName[0]].keys():
                outData[listedName[0]][listedName[1]] = {}
            if listedName[2] not in outData[listedName[0]][listedName[1]].keys():
                outData[listedName[0]][listedName[1]][listedName[2]] = {}
            if listedName[2] not in outData[listedName[0]][listedName[1]][listedName[2]].keys():
                outData[listedName[0]][listedName[1]][listedName[2]][listedName[3]] = {}
            outData[listedName[0]][listedName[1]][listedName[2]][listedName[3]]["".join(listedName[4:])] = item

        if len(listedName) > 5:
            if listedName[0] not in outData.keys():
                outData[listedName[0]] = {}
            if listedName[1] not in outData[listedName[0]].keys():
                outData[listedName[0]][listedName[1]] = {}
            if listedName[2] not in outData[listedName[0]][listedName[1]].keys():
                outData[listedName[0]][listedName[1]][listedName[2]] = {}
            if listedName[2] not in outData[listedName[0]][listedName[1]][listedName[2]].keys():
                outData[listedName[0]][listedName[1]][listedName[2]][listedName[3]] = {}
            if listedName[2] not in outData[listedName[0]][listedName[1]][listedName[2]][listedName[3]].keys():
                outData[listedName[0]][listedName[1]][listedName[2]][listedName[3]][listedName[4]] = {}
            outData[listedName[0]][listedName[1]][listedName[2]][listedName[3]][listedName[4]]["".join(listedName[5:])] = item


        if len(listedName) > 6:
            print("Baaa")
    return outData

class StructData():
    def __init__(self, Struct:dict, parent=None):
        if parent == None:
            parent = self
        for key, value in Struct.items():
            if type(value) == dict:
                setattr(parent, key, StructData(value))
            else:
                setattr(self, key, self.getPLCData(value))
    def __repr__(self):
        return str(str(self.__dict__.items()))

    def __iter__(self):
        for key in self.__dict__:
            yield key, getattr(self,key)

    def getPLCData(self, value):
        return value















if __name__ == '__main__':
    import pyclip
    Array = DataBlock_to_Array(pyclip.paste(text=True))
    Stuct = Array_to_Struct(Array)
    Data = StructData(Stuct)













