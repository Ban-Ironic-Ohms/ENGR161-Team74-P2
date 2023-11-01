# we need to represent the layout of the factory. Important peices are: 
# 1) unit operations ferm, dhyd, dist, and filt
# 2) LINKED LIST!!!!!!!!!
# 2) pumps, pipes, ductwork for gasses (waste), turns
# 3) valves

# we need to make a linked list that sends the solution between different THINGS (above)
# we also need an OPTIONAL output for waste that also costs but doesent eff, if that makes sense

# so, what do we do with these? we want some sense of cost (everything), 
# efficiency (everything maybe? basically, just a sense of how much energy it uses)

# the operators needs to have an associated function which you pass ANOTHER object (the solution)
# through to get the resultant solution

# QUESTION: will the different Operators be for the different options? 
# no. we will generate linked lists for each FULL PATH OPTIONS passing the name, eff, etc for each

# NOTE: efficiency of pumps needs to be investigated

# superclass for the "important peices"

import operationCalculations as oC

class Part():
    def __init__(self, name) -> None:
        self.name = name
        
        # these are used for the linked list
        self.next = None
        self.waste = None

class Operator(Part):
    def __init__(self, name, opType, costM3pH, power, eff, solnFunc) -> None:
        super().__init__(name)
        self.opType = opType
        self.power = power
        self.eff = eff
        self.costM3pH = costM3pH
        self.solnFunc = solnFunc
        
class Pump(Part):
    def __init__(self, name, costM3pH, profRating, eff) -> None:
        super().__init__(name)
        self.profRating = profRating
        self.eff = eff
        self.costM3pH = costM3pH
        
class Transfer(Part):
    def __init__(self, name, diameter) -> None:
        super().__init__(name)
        self.diameter = diameter
        
class Pipe(Transfer):
    def __init__(self, name, darcyFrictionFactor, costM, length, diameter) -> None:
        super().__init__(name, diameter)
        self.costM = costM
        self.eff = darcyFrictionFactor
        self.length = length
    
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
        super().__init__(name)
        self.angle = angle
        self.pipeLoss = pipeLoss
        self.costPer = costPer
        self.diameter = diameter
    
class Valve(Part):
    def __init__(self, name, flowCoef, costPer, diameter) -> None:
        super().__init__(name)
        self.costPer = costPer
        self.diameter = diameter
        self.flowCoef = flowCoef

# STRUCTURE RULES:
# 1) each operator must have a valve on its inlet and outlet
# 2) each valve/pipe/bend connection must have the same diamter

# While I know how to make a linked list, I did maybe forget, so this is loosly based on 
# https://github.com/M2skills/Linked-List-in-Python/blob/master/LinkedList.py

class Node:
    def __init__(self, data=None) -> None:
        self.data = data
        self.next = None
    
    def getNextNode(self):
        return self.next
    
    def setNext(self, next):
        self.next = next
        
class Layout:
    def __init__(self) -> None:
        self.head = Node(Pipe("INPUT PIPE", 0, 0, 0, 0))
    
    def add(self, object):
        start = self.head
        tempNode = Node(object)
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
            curr = self.head
        
        if not issubclass(type(curr.getNextNode().data), Transfer):
            print("NOT A SUBCLASS")
            if not issubclass(type(curr.data), Transfer):
                self.checkDiameters(curr.getNextNode())
            

        
        if not diam:
            diam = curr.data.diameter
        
        if curr.next == None:
            print("CASE 1")
            return True
        elif diam != curr.next.data.diameter:
            print("CASE 2")
            
            return False
        else:
            return self.checkDiameters(curr.getNextNode(), diam)
        
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

print(a.printList())
print(a.checkDiameters())
