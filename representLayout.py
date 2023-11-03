# we need to represent the layout of the factory. Important peices are: 
# 1) unit operations ferm, dhyd, dist, and filt
# 2) LINKED LIST!!!!!!!!!
# 2) pumps, pipes, ductwork for gasses (waste), turns
# 3) valves

# we need to make a linked list that sends the solution between different THINGS (above)
# we also need an OPTIONAL output for waste that also costs but doesent eff, if that makes sense

# so, what do we do with these? we want some sense of cost (everything), 
# efficiency (everything maybe? basically, just a sense of how much energy it uses)

# the operators needs t9.81o have an associated function which you pass ANOTHER object (the solution)
# through to get the resultant solution

# QUESTION: will the different Operators be for the different options? 
# no. we will generate linked lists for each FULL PATH OPTIONS passing the name, eff, etc for each

# superclass for the "important peices"


import operationCalculations as oC
import numpy as np
import itertools
import math
import time

# INITIAL_MASS_FLOW = oC.Solution(100000)
GRAVITY = 9.81

class Part():
    def __init__(self, name) -> None:
        self.name = name

        
class Operator(Part):
    def __init__(self, name, opType, costM3pH, power, eff, solnFunc) -> None:
        super().__init__(name)
        self.opType = opType
        self.power = power
        self.eff = eff
        self.costM3pH = costM3pH
        self.solnFunc = solnFunc
        
    def solveMass(self, massFlow):
        return self.solnFunc(self.eff, massFlow)
    
    def calculateCost(self, massFlow):
        return self.costM3pH * massFlow.massFlowRate()
    
    def calculatePower(self, *args):
        return self.power
        
class Pump(Part):
    def __init__(self, name, costM3pH, profRating, eff) -> None:
        super().__init__(name)
        self.profRating = profRating
        self.eff = eff
        self.costM3pH = costM3pH
    
    def calculateCost(self, massFlow):
        return self.costM3pH * massFlow.massFlowRate()
    
    def calculatePower(self, height, massFlow, density): # returns kJ per day
        return self.eff * height * GRAVITY * massFlow.massFlowRate() * density * 24 * 1/1000
    
class Transfer(Part):
    def __init__(self, name, diameter) -> None:
        super().__init__(name)
        self.diameter = diameter
    
    def __str__(self) -> str:
        return f"diameter: {self.diameter}"

    def calculatePower(self, *args):
        return 0
        
class Pipe(Transfer):
    def __init__(self, name, darcyFrictionFactor, costM, length, diameter) -> None:
        super().__init__(name, diameter)
        self.costM = costM
        self.eff = darcyFrictionFactor
        self.length = length
    
    def calculateCost(self, *args):
        return self.length * self.costM

    # built on Darcy-Weisbach Equn from slides
    def headLoss(self, massFlow):
        return self.eff * (8 * massFlow.massFlowRate()**2 * self.length) * (1 / (math.pi**2 * GRAVITY * self.diameter**5))
    
class Duct(Pipe):
    def __init__(self, name, costM, length, diameter) -> None:
        super().__init__(name, 0.002, costM, length, diameter)
        
class Bend(Transfer):
    def __init__(self, name, angle, pipeLoss, costPer, diameter) -> None:
        """
        Creates a Bend object
        
        Args:
            name (str): The name of the type of bend (average, nice).
            angle (int): The angle of the bend in degrees.
            pipeLoss (float): the pipe loss coefficent.
            costPer (float): the cost per bend piece.
            diameter (float): the internal diameter of the bend

        Returns:
            None
        """
        super().__init__(name, diameter)
        self.angle = angle
        self.pipeLoss = pipeLoss
        self.costPer = costPer
    
    def calculateCost(self, *args):
        return self.costPer

    # from slides
    def headLoss(self, massFlow):
        return self.pipeLoss * (massFlow.massFlowRate() / (math.pi * self.diameter**2))**2 * (1 / (2 * GRAVITY))
    
class Valve(Transfer):
    def __init__(self, name, flowCoef, costPer, diameter) -> None:
        super().__init__(name, diameter)
        self.costPer = costPer
        self.flowCoef = flowCoef
    
    def calculateCost(self, *args):
        return self.costPer
    
    # from slides
    def headLoss(self, massFlow):
        return self.flowCoef * (massFlow.massFlowRate() / (math.pi * self.diameter**2))**2 * (1 / (2 * GRAVITY))

# STRUCTURE RULES:
# 1) each operator must have a valve on its inlet and outlet
# 2) each valve/pipe/bend connection must have the same diamter

# While I know how to make a linked list, I did maybe forget, so this is loosly based on 
# https://github.com/M2skills/Linked-List-in-Python/blob/master/LinkedList.py

class Node:
    def __init__(self, data=None, massFlow = 0) -> None:
        self.data = data
        self.massFlow = massFlow
        self.next = None
        self.waste = None
    
    def getNextNode(self):
        return self.next
    
    def setNext(self, next):
        self.next = next
        
class Layout:
    def __init__(self, staticHead) -> None:
        self.head = Node(Pipe("INPUT PIPE", 0, 0, 0, 1), oC.Solution(100)) # initial diam = 1 because otherwise it breaks
        
        self.staticHead = staticHead
        self.score = None
    
    def add(self, object, massFlow):
        start = self.head
        tempNode = Node(object, massFlow)
        while start.getNextNode():
            start = start.getNextNode()
        start.setNext(tempNode)
        del tempNode
        return True
    
    def addWaste(self, object):
        pass
    # TODO!!
    
    def printList(self):
        start = self.head
        finalString = ""
        while start:
            tempString = start.data.name
            finalString += str(tempString)
            start = start.getNextNode()

            # if next node exists only the append seperator
            if start:
                finalString += " -- "

        return finalString

    def getLastNode(self): 
        curr = self.head
        while curr.getNextNode():
            curr = curr.getNextNode()
        
        return curr
    
    def __str__(self) -> str:
        return self.printList()
    
    def fullPrint(self) -> str:
        return f"LAYOUT: {self.printList()}\nPOWER: {self.layoutPower()} / day\nHEAD: {self.layoutEffectiveHead()} m\nSTATIC COST: ${self.layoutStaticCost()}\nCOST PER DAY: ${self.layoutMFRCost()}\nETHANOL CONCENTRATION: {self.ethanolConcentration()}%\nETHANOL AMOUNT: {self.ethanolAmount()} m^3/day"
    
    def checkDiameters(self, start=None, diam=None):
        curr = start
        if not start:
            # print("Starting the recursion with head")
            curr = self.head
            
        if curr.next == None:
            # print("ENDING! We it works!")
            return True
        
        # print(f"\nCalling func with start {curr.data.name} and diam {diam}")
        
        if not issubclass(type(curr.getNextNode().data), Transfer):
            # print("The next node in the chain is not a sublcass. Skipping 2 fwrd")
            return self.checkDiameters(curr.getNextNode().getNextNode())
        
        if not issubclass(type(curr.data), Transfer):
            # print(f"THIS node {curr.data} is not a subclass({type(curr.data)} not Transfer). SKipping 1 fwrd")
            return self.checkDiameters(curr.getNextNode())
            
        # at this point, this node and the next node are subclasses
        
        if not diam:
            diam = curr.data.diameter
            
        # print(f"Diam: {diam}")
        if diam != curr.getNextNode().data.diameter:
            # print("CASE 2")   
            return False
        else:
            return self.checkDiameters(curr.getNextNode(), diam)

    # returns the initial cost to create the layout
    def layoutStaticCost(self):
        curr = self.head
        cost = 0
        while curr:
            if issubclass(type(curr.data), Transfer):
                cost += curr.data.calculateCost(curr.massFlow)
            curr = curr.getNextNode()

        return cost
    
    # returns the cost the run the layout PER DAY
    def layoutMFRCost(self):
        curr = self.head
        cost = 0
        while curr:
            if issubclass(type(curr.data), Operator) or issubclass(type(curr.data), Pipe):
                cost += curr.data.calculateCost(curr.massFlow)
            curr = curr.getNextNode()
            
        return cost * 24
    
    def layoutPower(self):
        curr = self.head
        power = 0
        while curr:
            power += curr.data.calculatePower(self.layoutEffectiveHead(), curr.massFlow, curr.massFlow.density())
            curr = curr.getNextNode()
        
        return power
            
    def layoutEffectiveHead(self):
        head = self.staticHead
        
        curr = self.head
        while curr:
            if issubclass(type(curr.data), Transfer):
                head += curr.data.headLoss(curr.massFlow)
            curr = curr.getNextNode()
        
        return head
    
    def ethanolConcentration(self):
        last = self.getLastNode()
        
        return last.massFlow.ethanolConcentration()
    
    # returns the amount of ethanol PER DAY
    def ethanolAmount(self):
        last = self.getLastNode()
        return last.massFlow.ethanol * 24
        
    def layoutScore(self, minPow, maxPow, minStatCost, maxStatCost, minOpCost, maxOpCost):
        if self.ethanolConcentration() < 0.98:
            self.score = 0
            return self.score
        
        power = (self.layoutPower() - minPow) / (maxPow - minPow)
        staticCost = (self.layoutStaticCost() - minStatCost) / (maxStatCost - minStatCost)
        operatingCost = (self.layoutMFRCost() - minOpCost) / (maxOpCost - minOpCost)

        score = power - staticCost - operatingCost
        
        self.score = score
        return score

"""
# ----------------- GENERATE SPACE OF ALL POSSIBILITIES -------------------

#        ---- create lists of options for each part ----
def ferment():
    fid = open('data/fermenters.csv', 'r')
    header = fid.readline()
    headers = header.strip().split(',')
    rawData = fid.readlines()
    fid.close()
    data = [i.strip().split(',') for i in rawData] # can't cast to int because i.split() gives a list
    fermented = []
    for i in range(len(data[0])):
        fermented.append(Operator(headers[i], "Fermenter", float(data[0][i]), float(data[1][i]), float(data[2][i]), oC.fermenter))
    return fermented

def pumps():
    fid = open('data/pumps.csv', 'r')
    header = fid.readline()
    headers = header.strip().split(',')
    rawData = fid.readlines()
    data = [i.strip().split(",") for i in rawData]
    fid.close()
    pumps = []
    for i in range(1, len(data)):
        temp = []
        for j in range(1,data[i].length()):
            temp.append(Pump(headers[j],float(data[i][j]),float(data[i][0]),int(data[0][j]))) 
        pumps.append(temp)
    return pumps

#           ---- lists used for testing (remove later) ----
operators = [Operator("Scrap", "Fermenter", 320, 46600, 0.5, oC.fermenter), Operator("Average", "Fermenter", 380, 47200, 0.75, oC.fermenter),]
pumps1 = [Pump("Cheap", 260, 6, 1), Pump("Value", 200, 1, 6), Pump("Casdheap", 200, 1, 6)]
    # [Pump("Cheap", 200, 1, 9), Pump("Value", 200, 1, 9), Pump("asd", 200, 1, 9)],   
# ]
bends = [Bend("120", 90, 120, 23, 0.1), Bend("100", 90, 100, 23, 0.1), Bend("80", 90, 80, 23, 0.1)]

# print(ferment())
# print(pumps())

#           ---- create the generic layout
generic = [ferment(), pumps1, bends]
generic = [ferment() for i in range(4)]
transferDiameters = [.1, 0.13]

def generateLayoutSpace(generic, transferDiameters, staticHead):
    lengths = tuple([len(i) for i in generic])

    shape = [lengths[i] for i in range(len(lengths))]

    allPossibleLayouts = np.zeros(lengths, dtype=np.object_)

    for idx in itertools.product(*[range(s) for s in shape]):
        print("NEW LAYOUT")
        createdLayout = Layout(staticHead)
        currentMassFlow = createdLayout.head.massFlow
        print(currentMassFlow)
        
        time.sleep(0.1)
        for genericIndex, partKey in enumerate(idx):
            partToAdd = generic[genericIndex][partKey]
            if issubclass(type(partToAdd), Operator):
                # print("applying a fermenter to soln")
                currentMassFlow = partToAdd.solveMass(currentMassFlow)
                print(currentMassFlow)
                # time.sleep(1)
            createdLayout.add(generic[genericIndex][partKey], currentMassFlow) 
            
        allPossibleLayouts[idx] = createdLayout

    return allPossibleLayouts

layoutSpace = generateLayoutSpace(generic, transferDiameters, 100000)
# print(layoutSpace)

start = time.time()

for layout in layoutSpace.flatten():
    print(layout.printList())
    print("POWER", layout.layoutPower())
    print("HEAD", layout.layoutEffectiveHead())
    print("COST", layout.layoutCost())
    # print("DIAMETER CHECK:", layout.checkDiameters())
    print("")
    pass
    
print(f"run took {time.time() - start} sec")


# later I should add waste outputs
a = Layout(10)
a.add(Pump("Pump1", 415, 6, 0.92), INITIAL_MASS_FLOW) # NOTE: we will have to forward calculate the necessary effective elevation gain (similar to how we calculate if the sequential diamteres work)
a.add(Pipe("Pipe2", 0.002, 2.97, 0, 0.1), INITIAL_MASS_FLOW)
a.add(Operator("OP3", "Fermenter", 380, 47200, 0.75, oC.fermenter), INITIAL_MASS_FLOW)
a.add(Valve("Valve4", 800, 1, 0.1), INITIAL_MASS_FLOW)
a.add(Pipe("Pipe5", 0.01, 2.16, 1.524, 0.1), INITIAL_MASS_FLOW)
a.add(Valve("Valve6", 800, 1, 0.1), INITIAL_MASS_FLOW)
a.add(Operator("Op7", "Filtration", 240, 49536, 0.75, oC.filt), INITIAL_MASS_FLOW)
a.add(Valve("Valve8", 800, 1, 0.1), INITIAL_MASS_FLOW)
a.add(Pump("Pump9", 415, 6, 0.92), INITIAL_MASS_FLOW)
a.add(Pipe("Pipe10", 0.01, 2.16, 3.048, 0.1), INITIAL_MASS_FLOW)
a.add(Valve("Valve11", 800, 1, 0.1), INITIAL_MASS_FLOW)
a.add(Operator("Op12", "Distiller", 460, 47812, 0.9, oC.distiller), INITIAL_MASS_FLOW)
a.add(Valve("Valve13", 800, 26, 0.15), INITIAL_MASS_FLOW)
a.add(Pump("Pump14", 415, 6, 0.92), INITIAL_MASS_FLOW)
a.add(Pipe("Pip15", 0.01, 55, 3.048, 0.15), INITIAL_MASS_FLOW) #change 0.15 -> 0.1 to check the checkDiamter func
a.add(Valve("Valve16", 800, 26, 0.15), INITIAL_MASS_FLOW)
a.add(Operator("Op17", "Dehydrator", 240, 49536, 0.75, oC.dehydrator), INITIAL_MASS_FLOW)
a.add(Valve("Valve18", 800, 26, 0.15), INITIAL_MASS_FLOW)
a.add(Pipe("Pip19", 0.01, 55, 3.048, 0.15), INITIAL_MASS_FLOW) 
# END!
print(a.printList())
print(a.checkDiameters())
print(a.layoutCost())
print(a.layoutEffectiveHead())



"""