from representLayout import *
import functools

# ----------------- GENERATE SPACE OF ALL POSSIBILITIES -------------------


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

def pumps(profRating = 0):
    profRating = 36
    fid = open('data/pumps.csv', 'r')
    header = fid.readline()
    headers = header.strip().split(',')
    rawData = fid.readlines()
    data = [i.strip().split(",") for i in rawData]
    fid.close()
    pumps = []
    for i in range(0, len(data)):
        temp = []
        for j in range(1, len(data[i])): 
            temp.append(Pump(headers[j], float(data[i][j]), float(data[i][0]), float(data[0][j]))) 
        pumps.append(temp)
    if (profRating):
        diam = [0, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
        pumps = pumps[diam.index(profRating)]
    return pumps

def bends(angle, diam):
    fid = open('data/bend.csv','r')
    header = fid.readline()
    anglesl = header.strip().split(',')
    anglesl = anglesl[1:]
    angles = [0,20.0,30.0,45.0,60.0,75.0,90.0]
    rawData = fid.readlines()
    data = [i.strip().split(',') for i in rawData]
    diams = [0,0.1,0.11,0.12,0.13,0.14,0.15]
    fid.close
    bend = [Bend(str(angle), angle, float(data[0][angles.index(angle)]), float(data[diams.index(diam)][angles.index(angle)]), diam)]
    return bend

def pipes(length, diam = None):
    fid = open('data/pipes.csv','r')
    header = fid.readline()
    headers = header.strip().split(',')
    rawData = fid.readlines()
    data = [i.strip().split(',') for i in rawData]
    fid.close()
    pipes = []
    for i in range(1, len(data)):
        temp = []
        for j in range(1,len(data[i])):
            temp.append(Pipe(headers[j], float(data[0][j]), float(data[i][j]), length, float(data[i][0])))
        pipes.append(temp)
    if (diam):
        n = [0.1,0.11,0.12,0.13,0.14,0.15]
        pipes = pipes[n.index(diam)]
    return pipes

def valves(diam):
    fid = open('data/valves.csv','r')
    header = fid.readline()
    headers = header.strip().split(",")
    rawData = fid.readlines()
    data = [i.strip().split(",") for i in rawData]
    fid.close
    valves = []
    for i in range(1, len(data)):
        temp = []
        for j in range(1, len(data[i])):
            temp.append(Valve(headers[j], float(data[0][j]), float(data[i][j]),diam))
        valves.append(temp)
    n = [0.1, 0.11, 0.12, 0.13, 0.14, 0.15]
    valves = valves[n.index(diam)]
    return valves

def ducts(diam, length):
    fid =  open('data/ducts.csv','r')
    fF = fid.readline()
    fricF = fF.strip().split(',')
    rawData = fid.readlines()
    data = [ i.strip().split(',') for i in rawData]
    diameter = []
    for i in range(len(data)):
        diameter.append(float(data[i][0]))
    duc = (Duct(str(diam), float(data[diameter.index(diam)][1]), length, diam))
    return [duc]



#           ---- create the generic layout ----

generic = [
    [Pump("Cheap", 290, 36, 0.8)],
    [Bend("90", 90, 0.3, 1.28, 0.1)],
    [Pipe("Nice", 0.01, 2.16, 15.24, 0.1)],
    [Bend("90", 90, 0.3, 1.28, 0.1)],
    [Valve("Salvage", 800, 1, 0.1)],
    [Operator("Scrap", "Fermenter", 320, 46600, 0.5, oC.fermenter)],
    # fermenters(),
    [Valve("Salvage", 800, 1, 0.1)],
    [Pipe("Nice", 0.01, 2.16, 10, 0.1)],
    [Valve("Salvage", 800, 1, 0.1)],
    [Operator("Scrap", "Filter", 200, 48800, 0.5, oC.filt)],
    [Valve("Salvage", 800, 1, 0.1)],
    [Pipe("Nice", 0.01, 2.16, 10.0, 0.1)],
    [Valve("Salvage", 800, 1, 0.1)],
    [Operator("Scrap", "Distiller", 390, 47004, 0.81, oC.distiller)],
    [Valve("Salvage", 800, 1, 0.1)],
    [Pipe("Nice", 0.01, 2.16, 10.0, 0.1)],
    [Bend("90", 90, 0.3, 1.28, 0.1)],
    [Bend("90", 90, 0.3, 1.28, 0.1)],
    [Valve("Salvage", 800, 1, 0.1)],
    [Operator("Scrap", "Dehydrator", 200, 48800, 0.5, oC.dehydrator)],
    [Valve("Salvage", 800, 1, 0.1)],
    [Pipe("Nice", 0.01, 2.16, 3.05, 0.1)],
    [Duct("1", 228, 1, 1)]
]



# generic = [fermenters(), filters(), pipes(10, 0.15), valves(0.15), distillers(), dehydrators(), valves(0.15), pipes(10, 0.15)]
stdDiam = 0.15
valveOpt = 3 # runs tell us this is best
generic = [pumps(36), [valves(stdDiam)[valveOpt]], fermenters(), [valves(stdDiam)[valveOpt]], pipes(10, stdDiam), [valves(stdDiam)[valveOpt]], filters(), [valves(stdDiam)[valveOpt]], bends(90, stdDiam), pipes(15, stdDiam), [valves(stdDiam)[valveOpt]], distillers(), [valves(stdDiam)[valveOpt]], pipes(10, stdDiam), [valves(stdDiam)[valveOpt]], dehydrators(), [valves(stdDiam)[valveOpt]], bends(90, stdDiam), pipes(10, stdDiam)]
# generic = [pumps(36), valves(stdDiam), fermenters(), valves(stdDiam), pipes(10, stdDiam), valves(stdDiam), filters(), valves(stdDiam), bends(90, stdDiam), pipes(15, stdDiam), valves(stdDiam), distillers(), valves(stdDiam), pipes(10, stdDiam), valves(stdDiam), dehydrators(), valves(stdDiam), bends(90, stdDiam), pipes(10, stdDiam)]

generic = [
    [Pump("Cheap", 510, 36, 0.8)],
    [Valve("Glorious", 500, 76, stdDiam)],
    [Operator("Premium", "Fermenter", 460, 47500, 0.9, oC.fermenter)],
    [Valve("Glorious", 500, 76, stdDiam)],
    [Pipe("Salvage", 0.05, 26, 10, stdDiam)],
    [Valve("Glorious", 500, 76, stdDiam)],
    [Operator("Premium", "Filter", 280, 50350, 0.9, oC.filt)],
    [Valve("Glorious", 500, 76, stdDiam)],
    [Bend("90", 90, 0.3, 80, stdDiam)],
    [Pipe("Salvage", 0.05, 26, 15, stdDiam)],
    [Valve("Glorious", 500, 76, stdDiam)],
    [Operator("Average", "Distiller", 460, 47812, 0.9, oC.distiller)],
    [Valve("Glorious", 500, 76, stdDiam)],
    [Pipe("Salvage", 0.05, 26, 10, stdDiam)],
    [Valve("Glorious", 500, 76, stdDiam)],
    [Operator("World Class", "Dehydrator", 480, 51000, 0.98, oC.dehydrator)],
    [Bend("90", 90, 0.3, 80, stdDiam)],
    [Valve("Glorious", 500, 76, stdDiam)],
    [Pipe("Salvage", 0.05, 26, 10, stdDiam)]
]

transferDiameters = [.1, 0.13]

#           ---- generate layout space ---
def generateLayoutSpace(generic, transferDiameters, staticHead, initialVFR):
    lengths = tuple([len(i) for i in generic])

    shape = [lengths[i] for i in range(len(lengths))]
    
    print(f"The number of possible layouts is {functools.reduce(lambda x, y: x*y, shape)}")

    allPossibleLayouts = np.zeros(lengths, dtype=np.object_)

    printBuffer = 0
    for idx in itertools.product(*[range(s) for s in shape]):
        if printBuffer % 10000 == 0:
            print("Generating idx", idx)
            printBuffer = 0
        printBuffer += 1
        # print("\nNEW LAYOUT")
        createdLayout = Layout(staticHead, initialVFR)
        currentMassFlow = createdLayout.head.massFlow
        # print(currentMassFlow)
        
        # time.sleep(0.1)
        
        for genericIndex, partKey in enumerate(idx):
            partToAdd = generic[genericIndex][partKey]
            createdLayout.add(generic[genericIndex][partKey], currentMassFlow) 
            
            if issubclass(type(partToAdd), Operator):
                currentMassFlow = partToAdd.solveMass(currentMassFlow)
                # print(currentMassFlow)
                
            
        allPossibleLayouts[idx] = createdLayout
    # print(allPossibleLayouts)
    return allPossibleLayouts

# print(layoutSpace)

#           --- apply score function to  ---

def bestScore(layoutSpace):
    layoutSpace = layoutSpace.flatten()
    minPow = layoutSpace[0].layoutPower()
    maxPow = layoutSpace[0].layoutPower()
    minStatCost = layoutSpace[0].layoutStaticCost()
    maxStatCost = layoutSpace[0].layoutStaticCost()
    # minOpCost = layoutSpace[0].layoutMFRCost()
    # maxOpCost = layoutSpace[0].layoutMFRCost()
    
    printBuffer = 0
    maxValueStart = time.time()
    # for count, layout in enumerate(layoutSpace[::int(len(layoutSpace) / 10000)]):
    for count, layout in enumerate(layoutSpace):
        if printBuffer % 10000 == 0:
            print(f"checking layout {count} for max score values. Average {((time.time() - maxValueStart) / (count + 1) ) * 1000:.6f} sec per thousand")
            printBuffer = 0
        printBuffer += 1
        
        if minPow > layout.layoutPower():
            minPow = layout.layoutPower()
        if maxPow < layout.layoutPower():
            maxPow = layout.layoutPower()
            
        if minStatCost > layout.layoutStaticCost():
            minStatCost = layout.layoutStaticCost()
        if maxStatCost < layout.layoutStaticCost():
            maxStatCost = layout.layoutStaticCost()

    
    maxScore = (-100, 0)
    
    scoreStart = time.time()
    for count, layout in enumerate(layoutSpace):
        if printBuffer % 10000 == 0:
            print(f"calculating score num {count}. Average {((time.time() - scoreStart) / (count + 1) )* 1000:.6f} sec per thosand")
            printBuffer = 0
        printBuffer += 1
        
        score = layout.layoutScore(minPow, maxPow + 1, minStatCost, maxStatCost + 1)
        if score > maxScore[0]:
            maxScore = (score, layout)

    return maxScore


#           --- view and calculate layout space ----
start = time.time()

# layoutSpace = generateLayoutSpace(generic, transferDiameters, 10, 189.27)
layoutSpace = generateLayoutSpace(generic, transferDiameters, 10, 118.62)

idxtime = time.time() - start

bestConfig = bestScore(layoutSpace)

scoretime = time.time() - start - idxtime

# print(bestConfig[0], bestConfig[1])
print("")
print(bestConfig[1].fullPrint())

print(f"\nrun took {time.time() - start} sec. IDX gen time {idxtime}, score time {scoretime}")
