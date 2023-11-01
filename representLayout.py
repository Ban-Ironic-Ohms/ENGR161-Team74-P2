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

# NOTE: efficiency of pumps needs to be investigated

# superclass for the "important peices"


import operationCalculations as oC
import numpy as np
import itertools

INITIAL_MASS_FLOW = 100
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
    
    def calculateCost(self, massFlow):
        return self.costM3pH * massFlow
    
    def calculatePower(self, *args):
        return self.power
        
class Pump(Part):
    def __init__(self, name, costM3pH, profRating, eff) -> None:
        super().__init__(name)
        self.profRating = profRating
        self.eff = eff
        self.costM3pH = costM3pH
    
    def calculateCost(self, massFlow):
        return self.costM3pH * massFlow
    
    def calculatePower(self, height, massFlow, density): # returns kJ per day
        return self.eff * height * GRAVITY * massFlow * density * 24 * 1/1000
    
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
    
class Valve(Transfer):
    def __init__(self, name, flowCoef, costPer, diameter) -> None:
        super().__init__(name, diameter)
        self.costPer = costPer
        self.flowCoef = flowCoef
    
    def calculateCost(self, *args):
        return self.costPer

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
    def __init__(self) -> None:
        self.head = Node(Pipe("INPUT PIPE", 0, 0, 0, 0), INITIAL_MASS_FLOW)
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
        
    def calculateLayoutCost(self):
        curr = self.head
        cost = 0
        while curr:
            cost += curr.data.calculateCost(curr.massFlow)
            curr = curr.getNextNode()

        return cost
    
    def calculatePower(self):
        curr = self.head
        power = 0
        while curr:
            power += curr.data.calculatePower(height, massflow, density)
    
    def calculateScore(self):
        self.score = 10
        return True
"""
# later I should add waste outputs
a = Layout()
a.add(Pump("Premium", 415, 6, 0.92)) # NOTE: we will have to forward calculate the necessary effective elevation gain (similar to how we calculate if the sequential diamteres work)
a.add(Pipe("Glorius", 0.002, 2.97, 0, 0.1))
a.add(Operator("Average", "Fermenter", 380, 47200, 0.75, oC.fermenter))
a.add(Valve("Salvage", 800, 1, 0.1))
a.add(Pipe("Nice", 0.01, 2.16, 1.524, 0.1))
a.add(Valve("Salvage", 800, 1, 0.1))
a.add(Operator("Average", "Filtration", 240, 49536, 0.75, oC.filt))
a.add(Valve("Salvage", 800, 1, 0.1))
a.add(Pump("Premium", 415, 6, 0.92))
a.add(Pipe("Nice", 0.01, 2.16, 3.048, 0.1))
a.add(Valve("Salvage", 800, 1, 0.1))
a.add(Operator("Average", "Distiller", 460, 47812, 0.9, oC.distiller))
a.add(Valve("Salvage", 800, 26, 0.15))
a.add(Pump("Premium", 415, 6, 0.92))
a.add(Pipe("Nice", 0.01, 55, 3.048, 0.15)) #change 0.15 -> 0.1 to check the checkDiamter func
a.add(Valve("Salvage", 800, 26, 0.15))
a.add(Operator("Average", "Dehydrator", 240, 49536, 0.75, oC.dehydrator))
a.add(Valve("Salvage", 800, 26, 0.15))
a.add(Pipe("Nice", 0.01, 55, 3.048, 0.15)) 
# END!
"""



# FERMENTERS [all possible Operators(""/)]
operators = [Operator("Scrap", "Fermenter", 320, 46600, 0.5, oC.fermenter), Operator("Average", "Fermenter", 380, 47200, 0.75, oC.fermenter),]
pumps = [
    [Pump("Cheap", 200, 1, 6), Pump("Value", 200, 1, 6), Pump("Casdheap", 200, 1, 6)],
    [Pump("Cheap", 200, 1, 9), Pump("Value", 200, 1, 9), Pump("asd", 200, 1, 9)],
    
]
bends = [Bend("asd", 90, 100, 23, 0.1), Bend("asd", 90, 100, 23, 0.1), Bend("asd", 90, 100, 23, 0.1)]


generic = [operators, pumps, bends]
transferDiameters = [.1, 0.13]
lengths = tuple([len(i) for i in generic])

shape = [lengths[i] for i in range(len(lengths))]

allPossibleLayouts = np.zeros(lengths, dtype=np.object_)

for idx in itertools.product(*[range(s) for s in shape]):
    createdLayout = Layout()
    currentMassFlow = createdLayout.head.massFlow
    for genericIndex, partKey in enumerate(idx):
        createdLayout.add(generic[genericIndex][partKey], massFlow=INITIAL_MASS_FLOW) # change later
        
    allPossibleLayouts[idx] = createdLayout


# later I should add waste outputs
a = Layout()
a.add(Pump("Pump1", 415, 6, 0.92), 10) # NOTE: we will have to forward calculate the necessary effective elevation gain (similar to how we calculate if the sequential diamteres work)
a.add(Pipe("Pipe2", 0.002, 2.97, 0, 0.1), 10)
a.add(Operator("OP3", "Fermenter", 380, 47200, 0.75, oC.fermenter), 10)
a.add(Valve("Valve4", 800, 1, 0.1), 10)
a.add(Pipe("Pipe5", 0.01, 2.16, 1.524, 0.1), 10)
a.add(Valve("Valve6", 800, 1, 0.1), 10)
a.add(Operator("Op7", "Filtration", 240, 49536, 0.75, oC.filt), 10)
a.add(Valve("Valve8", 800, 1, 0.1), 10)
a.add(Pump("Pump9", 415, 6, 0.92), 10)
a.add(Pipe("Pipe10", 0.01, 2.16, 3.048, 0.1), 10)
a.add(Valve("Valve11", 800, 1, 0.1), 10)
a.add(Operator("Op12", "Distiller", 460, 47812, 0.9, oC.distiller), 10)
a.add(Valve("Valve13", 800, 26, 0.15), 10)
a.add(Pump("Pump14", 415, 6, 0.92), 10)
a.add(Pipe("Pip15", 0.01, 55, 3.048, 0.15), 10) #change 0.15 -> 0.1 to check the checkDiamter func
a.add(Valve("Valve16", 800, 26, 0.15), 10)
a.add(Operator("Op17", "Dehydrator", 240, 49536, 0.75, oC.dehydrator), 10)
a.add(Valve("Valve18", 800, 26, 0.15), 10)
a.add(Pipe("Pip19", 0.01, 55, 3.048, 0.15), 10) 
# END!
print(a.printList())
print(a.checkDiameters())
print(a.calculateLayoutCost())

