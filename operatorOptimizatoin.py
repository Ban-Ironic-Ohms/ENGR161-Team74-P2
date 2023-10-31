import json
import numpy as np
import operationCalculations as oC
import time
import csv

start = time.time()

def loadJSONData(filepath):
    with open(filepath, "r") as file:
        return json.load(file)
    
def loadCSVData(filepath):
    return np.genfromtxt(filepath, delimiter=", ")
    
opsData = loadJSONData("data/operators.json")
pumpData = loadCSVData("data/pumps.csv")
pumpEff = pumpData[:1,1:][0]
pumpLen = [i[0] for i in pumpData[1:,:1]]
pumpData = pumpData[1:,1:]
print(pumpData)

# maybe add a class for mpumps/pipes etc?

class result:
    def __init__(self, ferm, dist, filt, dhyd, pump, eff=0, cost=0, power=0) -> None:
        self.ferm = ferm
        self.dist = dist
        self.filt = filt
        self.dhyd = dhyd
        
        self.pump = pump
        
        self.eff = eff
        self.cost = cost
        self.power = power
    
    def __eq__(self, other) -> bool:
        if self.eff != other.eff:
            return False
        if self.cost != other.cost:
            return False
        if self.power != other.power:
            return False
        return True

    def scoreCompare(self, other):
        print("-----SCORE COMPARE-----")
        maxEff = max(self.eff, other.eff)
        minCost = min(self.cost, other.cost)
        minEnergy = min(self.power, other.power)
        
        print(f"between {self.eff} and {other.eff} we chose {maxEff} as the max")
        print(f"between {self.cost} and {other.cost} we chose {minCost} as the min")
        print(f"between {self.power} and {other.power} we chose {minEnergy} as the min")

        selfScore = (self.eff / maxEff) + (self.cost / minCost) + (self.power / minEnergy)
        otherScore = (other.eff / maxEff) + (other.cost / minCost) + (other.power / minEnergy)
        
        print(f"Self score {selfScore}")
        print(f"Other score {otherScore}")

        return (selfScore, otherScore)
    
    def __lt__(self, other) -> bool:
        scores = self.scoreCompare(other)
        return (scores[0] < scores[1])
    
    def __le__(self, other) -> bool:
        scores = self.scoreCompare(other)
        return (scores[0] <= scores[1]) 
       
    def __gt__(self, other) -> bool:
        scores = self.scoreCompare(other)
        return (scores[0] > scores[1])
    
    def __ge__(self, other) -> bool:
        scores = self.scoreCompare(other)
        return (scores[0] >= scores[1])  
    
    def __str__(self) -> str:
        return f"eff: {self.eff}, cost: ${self.cost}, energy: {self.power}kW for\
ferm:{self.ferm}, dist:{self.dist}, filt:{self.filt}, dhyd:{self.dhyd}, pump:\
{self.pump}"

def calculateEff(data, pumpEff, ferm, dist, filt, dhyd, pump):
    # print(data["Fermenters"][ferm]), 
    ferm_eff = data["Fermenters"][ferm]["Efficiency"]
    dist_eff = data["Distillation Units"][dist]["Efficiency"]
    filt_eff = data["Filtration and Dehydration"][filt]["Efficiency"]
    dhyd_eff = data["Filtration and Dehydration"][dhyd]["Efficiency"]
    pump_eff = pumpEff[pump]
    return(ferm_eff * dist_eff * filt_eff * dhyd_eff * pump_eff)

def calculateCost(data, pumpData, ferm, dist, filt, dhyd, pump):
    ferm_cost = data["Fermenters"][ferm]["Cost"]
    dist_cost = data["Distillation Units"][dist]["Cost"]
    filt_cost = data["Filtration and Dehydration"][filt]["Cost"]
    dhyd_cost = data["Filtration and Dehydration"][dhyd]["Cost"]
    pump_cost = pumpData[pump]
    return(ferm_cost + dist_cost + filt_cost + dhyd_cost + pump_cost)

def calculatePower(data, ferm, dist, filt, dhyd):
    ferm_power = data["Fermenters"][ferm]["Energy Usage"]
    dist_power = data["Distillation Units"][dist]["Energy Usage"]
    filt_power = data["Filtration and Dehydration"][filt]["Energy Usage"]
    dhyd_power = data["Filtration and Dehydration"][dhyd]["Energy Usage"]
    return(ferm_power + dist_power + filt_power + dhyd_power)

# pumpLenNeeded = float(input("Min necessary pump power in m: "))
pumpLenNeeded = 32
for ind, i in enumerate(pumpLen):
    if i >= pumpLenNeeded:
        pumpData = pumpData[ind]
        break
        


results = np.zeros((4, 4, 4, 4, 5), dtype=np.object_)
for ferm in range(4):
    for dist in range(4):
        for filt in range(4):
            for dhyd in range(4):
                for pump in range(5):
                    results[ferm][dist][filt][dhyd][pump] = result(opsData["Fermenters"][ferm]["Name"], opsData["Distillation Units"][dist]["Name"], opsData["Filtration and Dehydration"][filt]["Name"], opsData["Filtration and Dehydration"][dhyd]["Name"], "NAME TBD COSTS " + str(pumpData[pump]), calculateEff(opsData, pumpEff, ferm, dist, filt, dhyd, pump), calculateCost(opsData, pumpData, ferm, dist, filt, dhyd, pump), calculatePower(opsData, ferm, dist, filt, dhyd))



print(results.flatten()[np.argmax(results)])

print(f"{round(time.time() - start, 5)} seconds")