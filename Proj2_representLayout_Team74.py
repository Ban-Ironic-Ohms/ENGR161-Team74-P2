# Project 2: Modeling Mass and Energy Balances
# File: Proj2_representLayout_Team74.py
# Date: 5 November 2023
# By: Micah Robinson
# robin709
# Mitchell McCormick 
# mccorm84
# Amanda Zheng 
# zheng749
# Savannah Hoar
# shoar
# Section: 5
# Team: 74
#
# ELECTRONIC SIGNATURE
# Micah Robinson
# Mitchell McCormick 
# Amanda Zheng 
# Savannah Hoar
#
# The electronic signatures above indicate that the program
# submitted for evaluation is the combined effort of all
# team members and that each member of the team was an
# equal participant in its creation. In addition, each
# member of the team has a general understanding of
# all aspects of the program development and execution.
#
# This program creates a framework for modeling a system of arbitrary components
# in a linear arrangment of class objects.

# This program refrenced outside code for the linked list implimentation

# ----------------- IMPORTS -------------------

import Proj2_operationCalculations_Team74 as oC
import numpy as np
import itertools
import math
import time

# ----------------- CONSTANTS -------------------

GRAVITY = 9.81

# ----------------- CLASSES FOR EQUIPMENT -------------------

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
    
    def calculatePower(self, *args):
        if self.length == 0: #input pipe
            return 0
        
        # --- pipe vibration energy loss modeled as power usage ---
        # These values come from research and assumptions listed in poster
        speedSound = 3230
        youngMod = 29.5
        possionRatio = 0.29
        outerDiam = 0.5
        deflectionFactor = 0.05
        
        energy = (speedSound * youngMod * (self.diameter + outerDiam) * (deflectionFactor * self.length * possionRatio)**2) * (1 / (2 * self.length**2))
        # return 0
        return energy
    
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
 
 # ----------------- REPRESENT LAYOUT AS LINKED LIST -------------------

# CODE FROM EXTERNAL SOURCE

# Basic linked list and basic implimentation refrenced from my (Micah's) own code:
# https://github.com/Ban-Ironic-Ohms/2021-tide-py/blob/master/Intro/linkedListsandDict.py

# no code was directly copied, though a linked list implimentaiton is fairly standard
# source was used for the implimentation of the __init__ method in Node and printList method in Layout.

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
    
    def printList(self):
        curr = self.head
        finalString = ""
        while curr:
            tempString = curr.data.name + " " + str(type(curr.data))[24:-2]
            
            # tempString += f"{vars(curr.data)}\n{vars(curr.massFlow)}\n\n"
            finalString += str(tempString)
            curr = curr.getNextNode()

            # if next node exists only the append seperator
            if curr:
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
        return f"LAYOUT: {self.printList()}\n\
POWER: {self.layoutPower():.3f} / kJ day\n\
HEAD: {self.layoutEffectiveHead():.3f} m\n\
STATIC COST: ${self.layoutStaticCost():.2f}\n\
ETHANOL CONCENTRATION: {self.ethanolConcentration()*100:.3f}%\n\
PURE ETHANOL AMOUNT: {self.ethanolAmount():.3f} m^3/day\n\
TOTAL SOLUTION AMOUNT: {self.endVFR():.4f} m^3/day\n\
SCORE: {self.score}\nENERGY ROI: {self.returnOI()}\n\
PURE ETHANOL AMT GAL: {self.ethanolAmount() * 264.2:.3f} gal/day\n\
ENERGY OUT: {self.ethanolAmount() * 264.2 * 80.1 * 1000:.3f} kJ/day\n\
fin. sltn. comp.: {self.getLastNode().massFlow}\n\
AGGREGATE WASTE: {self.getLastNode().massFlow.waste}"
    
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
            # print(vars(curr.massFlow))
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
        
        # print(f"calculating score")
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
        
        score = rOI + purity - power - staticCost
        
        self.score = score
        return score
