from representLayout import *

# ----------------- GENERATE SPACE OF ALL POSSIBILITIES -------------------
'''

#        ---- create lists of options for each part ----
# There will be a function for each object
def fermenters():
    fid = open('data/fermenters.csv', 'r')
    header = fid.readline()
    headers = header.strip().split(',')
    rawData = fid.readlines()
    fid.close()
    # data has rows of NAME, COST, POWER, EFF
    data = [i.strip().split(',') for i in rawData] 
    fermObjs = []
    for i in range(len(data[0])):
        fermObjs.append(Operator(headers[i], "Fermenter", float(data[0][i]), float(data[1][i]), float(data[2][i]), oC.fermenter))
    return fermObjs

def distillers():
    fid = open("data/distillers.csv", "r")
    header = fid.readline()
    headers = header.strip().split(',')
    rawData = fid.readlines()
    fid.close()
    # data has rows of NAME, COST, POWER, EFF
    data = [i.strip().split(',') for i in rawData] 
    distObjs = []
    for i in range(len(data[0])):
        distObjs.append(Operator(headers[i], "Distiller", float(data[0][i]), float(data[1][i]), float(data[2][i]), oC.distiller))
    return distObjs

def dehydrators():
    fid = open("data/dehydratorsFilters.csv", "r")
    header = fid.readline()
    headers = header.strip().split(',')
    rawData = fid.readlines()
    fid.close()
    # data has rows of NAME, COST, POWER, EFF
    data = [i.strip().split(',') for i in rawData] 
    dhydObjs = []
    for i in range(len(data[0])):
        dhydObjs.append(Operator(headers[i], "Dehydrator", float(data[0][i]), float(data[1][i]), float(data[2][i]), oC.dehydrator))
    return dhydObjs

def filters():
    fid = open("data/dehydratorsFilters.csv", "r")
    header = fid.readline()
    headers = header.strip().split(',')
    rawData = fid.readlines()
    fid.close()
    # data has rows of NAME, COST, POWER, EFF
    data = [i.strip().split(',') for i in rawData] 
    filtObjs = []
    for i in range(len(data[0])):
        filtObjs.append(Operator(headers[i], "Filter", float(data[0][i]), float(data[1][i]), float(data[2][i]), oC.filt))
    return filtObjs
    
def pumps(profRating = None):
    fid = open('data/pumps.csv', 'r')
    header = fid.readline()
    headers = header.strip().split(',')
    rawData = fid.readlines()
    data = [i.strip().split(",") for i in rawData]
    fid.close()
    pumps = []
    for i in range(1, len(data)):
        temp = []
        for j in range(1, len(data[i])): 
            temp.append(Pump(headers[j], float(data[i][j]), float(data[i][0]), float(data[0][j]))) 
        pumps.append(temp)
    if (profRating):
        diam = [0, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
        pumps = pumps[diam.index(profRating)]
    return pumps


def pipes(length, diam = None):
    fid = open('data/pipes.csv','r')
    header = fid.readline()
    headers = header.strip().split(',')
    rawData = fid.readlines()
    data = [i.strip().split(',') for i in rawData]
    fid.close()
    pipes = []
    for i in range(2, len(data)):
        temp = []
        for j in range(1,len(data[i])):
            temp.append(Pipe(headers[j], float(data[i][j]), float(data[1][j]), length, float(data[i][0])))
        pipes.append(temp)
    if (diam):
        n = [0,0.1,0.11,0.12,0.13,0.14,0.15]
        pipes = pipes[n.index(diam)]
    return pipes
'''
def bends(angle, diam):
    fid = open('data/bend.csv','r')
    header = fid.readline()
    anglesl = header.strip().split(',')
    anglesl = anglesl[1:]
    angles = [20.0,30.0,45.0,60.0,75.0,90.0]
    rawData = fid.readlines()
    data = [i.strip().split(',') for i in rawData]
    diams = []
    for i in range(1,len(data)):
        diams.append(float(data[i][0]))
        data[i] = data[i][1:]
    bend = Bend(str(angle),angle, float(data[0][angles.index(angle)]), data[diams.index(diam)][angles.index(angle)],diam)
    return [bend]
print(bends(30.0,0.1))
'''
    
#           ---- lists used for testing (remove later) ----
operators = [Operator("Scrap", "Fermenter", 320, 46600, 0.5, oC.fermenter), Operator("Average", "Fermenter", 380, 47200, 0.75, oC.fermenter),]
pumps1 = [Pump("Cheap", 260, 6, 1), Pump("Value", 200, 1, 6), Pump("Casdheap", 200, 1, 6)]
    # [Pump("Cheap", 200, 1, 9), Pump("Value", 200, 1, 9), Pump("asd", 200, 1, 9)],   
# ]
bends = [Bend("120", 90, 120, 25, 0.1), Bend("100", 90, 100, 23, 0.12), Bend("80", 90, 80, 199, 0.14)]

# print(fermenters())
# print(pumps())

#           ---- create the generic layout ----
generic = [fermenters(), filters(), distillers(), dehydrators()]
# generic = [fermenters() for i in range(4)]
transferDiameters = [.1, 0.13]

#           ---- generate layout space ---
def generateLayoutSpace(generic, transferDiameters, staticHead):
    lengths = tuple([len(i) for i in generic])

    shape = [lengths[i] for i in range(len(lengths))]

    allPossibleLayouts = np.zeros(lengths, dtype=np.object_)

    for idx in itertools.product(*[range(s) for s in shape]):
        # print("\nNEW LAYOUT")
        createdLayout = Layout(staticHead)
        currentMassFlow = createdLayout.head.massFlow
        # print(currentMassFlow)
        
        # time.sleep(0.1)
        
        for genericIndex, partKey in enumerate(idx):
            partToAdd = generic[genericIndex][partKey]
            if issubclass(type(partToAdd), Operator):
                currentMassFlow = partToAdd.solveMass(currentMassFlow)
                # print(currentMassFlow)
                
            createdLayout.add(generic[genericIndex][partKey], currentMassFlow) 
            
        allPossibleLayouts[idx] = createdLayout

    return allPossibleLayouts

layoutSpace = generateLayoutSpace(generic, transferDiameters, 10)
# print(layoutSpace)

#           --- apply score function to  ---

def bestScore(layoutSpace):
    layoutSpace = layoutSpace.flatten()
    minPow = layoutSpace[0].layoutPower()
    maxPow = layoutSpace[0].layoutPower()
    minStatCost = layoutSpace[0].layoutStaticCost()
    maxStatCost = layoutSpace[0].layoutStaticCost()
    minOpCost = layoutSpace[0].layoutMFRCost()
    maxOpCost = layoutSpace[0].layoutMFRCost()
    
    
    for layout in layoutSpace:
        if minPow > layout.layoutPower():
            minPow = layout.layoutPower()
        if maxPow < layout.layoutPower():
            maxPow = layout.layoutPower()
            
        if minStatCost > layout.layoutStaticCost():
            minStatCost = layout.layoutStaticCost()
        if maxStatCost < layout.layoutStaticCost():
            maxStatCost = layout.layoutStaticCost()
        
        if minOpCost > layout.layoutMFRCost():
            minOpCost = layout.layoutMFRCost()
        if maxOpCost < layout.layoutMFRCost():
            maxOpCost = layout.layoutMFRCost()
    
    maxScore = (-100, 0)
    
    for layout in layoutSpace:
        score = layout.layoutScore(minPow, maxPow + 1, minStatCost, maxStatCost + 1, minOpCost, maxOpCost + 1)
        if score > maxScore[0]:
            maxScore = (score, layout)

    return maxScore


bestConfig = bestScore(layoutSpace)
print(bestConfig[0], bestConfig[1])



#           --- view and calculate layout space ----
start = time.time()
works = 0
for layout in layoutSpace.flatten():
    print(layout.printList())
    print("POWER", layout.layoutPower(), "/ day")
    print("HEAD", layout.layoutEffectiveHead(), "m")
    print("STATIC COST $", layout.layoutStaticCost())
    print("COST PER DAY $", layout.layoutMFRCost())
    print("ETHANOL CONCENTRATION", layout.ethanolConcentration() * 100, "%")
    print("ETHANOL AMOUNT", layout.ethanolAmount(), "m^3/day")
    print("DIAMETER CHECK:", layout.checkDiameters())
    print("")
    if layout.ethanolConcentration() > 0.98:
        works += 1
    pass
print(f"{works} working layouts for 98% ethanol concentration")


bestConfig = bestScore(layoutSpace)
print(f"BEST: {bestConfig[1]} with score {bestConfig[0]} ")
print("BEST:")
print(bestConfig[1].fullPrint())

print(f"run took {time.time() - start} sec")