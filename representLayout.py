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
        self.power = power # in kWh/day
        self.eff = eff
        self.costM3pH = costM3pH
        self.solnFunc = solnFunc
        
    def solveMass(self, massFlow):
        return self.solnFunc(self.eff, massFlow)
    
    def setCost(self, massFlow):
        self.cost = self.costM3pH * massFlow.volumeFlowRate()
        # print(f"calculating cost FOR OPERATOR {self.costM3pH:.3f} * {massFlow.volumeFlowRate():.3f} = {self.cost:.3f}")
                    
    def calculateCost(self, *args):
        # print(f"returnign cost {self.cost}")
        return self.cost
    
    def calculatePower(self, *args): # returns kJ / h
        # print(f"adding power for operator of {self.power * (3600 / 24)} kJ/h")
        return self.power * (3600 / 24)
        
class Pump(Part):
    def __init__(self, name, costM3pH, profRating, eff) -> None:
        super().__init__(name)
        self.profRating = profRating
        self.eff = eff
        self.costM3pH = costM3pH
    
    def setCost(self, massFlow):
        self.cost = self.costM3pH * massFlow.volumeFlowRate()
        # print(f"calculatig cost FOR PUMP {self.costM3pH:.3f} * {massFlow.volumeFlowRate():.3f} = {self.cost:.3f}")
    
    def calculateCost(self, massFlow):
        # print(f"returning cost FOR PUMP {self.cost}")
        return self.cost
    
    def calculatePower(self, height, massFlow, density): # returns kJ per hour
        # print(f"PUMP POWER: {self.eff * height * GRAVITY * massFlow.massFlowRate() * (1/1000)} kJ/h")
        return self.eff * height * GRAVITY * massFlow.massFlowRate() * (1/1000) 
    
    def __str__(self):
        return f"{self.name} has cost {self.costM3pH} profRating {self.profRating} and eff {self.eff}"
    
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
        loss = self.eff * (8 * (massFlow.volumeFlowRate() / 3600)**2 * self.length) * (1 / (math.pi**2 * GRAVITY * (self.diameter / 2)**5))
        # print(f"--pipe head loss-- {loss}")
        return loss
    
    def __str__(self):
        return f"{self.name} has cost {self.calculateCost} flow coef {self.eff} and diam {self.diameter}"
    
class Duct(Pipe):
    def __init__(self, name, costM, length, diameter) -> None:
        super().__init__(name, 0.002, costM, length, diameter)
    def __str__(self):
        return f"{self.name} has cost {self.costM} length {self.length} and diam {self.diameter}"
    
        
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

    def __str__(self):
        return f"{self.name} has angle {self.angle} has cost {self.costPer} pipeloss {self.pipeLoss} and diam {self.diameter}"
    
    # from slides
    def headLoss(self, massFlow):
        loss = self.pipeLoss * ((massFlow.volumeFlowRate() / 3600) / (math.pi * (self.diameter / 2)**2))**2 * (1 / (2 * GRAVITY))
        # print(f"--bend head loss-- {loss}")
        return loss
    
class Valve(Transfer):
    def __init__(self, name, flowCoef, costPer, diameter) -> None:
        super().__init__(name, diameter)
        self.costPer = costPer
        self.flowCoef = flowCoef
    
    def calculateCost(self, *args):
        return self.costPer
    
    def __str__(self):
        return f"{self.name} has cost {self.costPer} flow coef {self.flowCoef} and diam {self.diameter}"
    
    # from slides
    def headLoss(self, massFlow):
        loss = self.flowCoef * ((massFlow.volumeFlowRate() / 3600)/ (math.pi * (self.diameter / 2)**2))**2 / ( (2 * GRAVITY))
        # print(f"--valve head loss-- {loss}")
        return loss
 
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
        
        if issubclass(type(data), Operator) or issubclass(type(data), Pump):
            self.data.setCost(massFlow)
    
    def getNextNode(self):
        return self.next
    
    def setNext(self, next):
        self.next = next
        
class Layout:
    def __init__(self, staticHead, initialVFR) -> None:
        self.head = Node(Pipe("INPUT PIPE", 0, 0, 0, 1), oC.Solution(initialVFR)) # initial diam = 1 because otherwise it breaks
        
        self.staticHead = staticHead
        self.score = None
    
    def add(self, object, massFlow):
        curr = self.head
        tempNode = Node(object, massFlow)
        while curr.getNextNode():
            curr = curr.getNextNode()
        curr.setNext(tempNode)
        del tempNode
        
        return True
    
    def addWaste(self, object):
        pass
    # TODO!!
    
    def printList(self):
        start = self.head
        finalString = ""
        while start:
            tempString = start.data.name + " " + str(type(start.data))[24:-2]
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
        return f"LAYOUT: {self.printList()}\nPOWER: {self.layoutPower():.3f} / kJ day\n\
HEAD: {self.layoutEffectiveHead():.3f} m\nSTATIC COST: ${self.layoutStaticCost():.2f}\n\
ETHANOL CONCENTRATION: {self.ethanolConcentration()*100:.3f}%\n\
PURE ETHANOL AMOUNT: {self.ethanolAmount():.3f} m^3/day\nTOTAL SOLUTION AMOUNT: {self.endVFR():.4f} m^3/day\n\
SCORE: {self.score}\nENERGY ROI: {self.returnOI()}\n\
PURE ETHANOL AMT GAL: {self.ethanolAmount() * 264.2:.3f} gal/day\n\
ENERGY OUT: {self.ethanolAmount() * 264.2 * 80.1 * 1000:.3f} kJ/day"
    
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
            # if issubclass(type(curr.data), Transfer):
            cost += curr.data.calculateCost(curr.massFlow)
            curr = curr.getNextNode()

        return cost
    
    # DEPRECIATED FUNCTION
    def layoutMFRCost(self):
        return 0
    
    # in kJ / day
    def layoutPower(self):
        curr = self.head
        power = 0
        while curr:
            power += curr.data.calculatePower(self.layoutEffectiveHead(), curr.massFlow, curr.massFlow.density())
            # print(f"adding power from {type(curr.data)} equal to {curr.data.calculatePower(self.layoutEffectiveHead(), curr.massFlow, curr.massFlow.density())}")
            curr = curr.getNextNode()
        
        return (power) * 24
            
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

    def endVFR(self):
        last = self.getLastNode()
        return last.massFlow.volumeFlowRate() * 24
    
    def returnOI(self):
        return (self.ethanolAmount() *  2.116E7) / self.layoutPower()
    
    def layoutScore(self, minPow, maxPow, minStatCost, maxStatCost):
        if self.ethanolConcentration() < 0.98:
            self.score = 0
            return self.score
        
        power = (self.layoutPower() - minPow) / (maxPow - minPow)
        staticCost = (self.layoutStaticCost() - minStatCost) / (maxStatCost - minStatCost)
        rOI = self.returnOI() / 10
        purity = (self.ethanolConcentration() - 0.98) / 0.02
        
        # --- weights ---
        power = power * 3
        staticCost = staticCost * 7
        rOI = rOI * 10
        purity = purity * 3
        
        score = power - staticCost + rOI + purity
        
        self.score = score
        return score
