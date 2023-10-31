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
    with open(filepath, newline="") as file:
        reader = csv.reader(file, delimiter=" ", quotechar="|")
        arr = np.array()
        for i in reader:
            print(i)
    
opsData = loadJSONData("data/operators.json")
pumpData = loadCSVData("data/pumps.csv")

class result:
    def __init__(self, ferm, dist, filt, dhyd, eff=0, cost=0, power=0) -> None:
        self.ferm = ferm
        self.dist = dist
        self.filt = filt
        self.dhyd = dhyd
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
        return f"eff: {self.eff}, cost: ${self.cost}, energy: {self.power}kW for ferm:{self.ferm}, dist:{self.dist}, filt:{self.filt}, dhyd:{self.dhyd}"

def calculateEff(data, ferm, dist, filt, dhyd):
    # print(data["Fermenters"][ferm])
    ferm_eff = data["Fermenters"][ferm]["Efficiency"]
    dist_eff = data["Distillation Units"][dist]["Efficiency"]
    filt_eff = data["Filtration and Dehydration"][filt]["Efficiency"]
    dhyd_eff = data["Filtration and Dehydration"][dhyd]["Efficiency"]
    return(ferm_eff * dist_eff * filt_eff * dhyd_eff)

def calculateCost(data, ferm, dist, filt, dhyd):
    ferm_cost = data["Fermenters"][ferm]["Cost"]
    dist_cost = data["Distillation Units"][dist]["Cost"]
    filt_cost = data["Filtration and Dehydration"][filt]["Cost"]
    dhyd_cost = data["Filtration and Dehydration"][dhyd]["Cost"]
    return(ferm_cost + dist_cost + filt_cost + dhyd_cost)

def calculatePower(data, ferm, dist, filt, dhyd):
    ferm_power = data["Fermenters"][ferm]["Energy Usage"]
    dist_power = data["Distillation Units"][dist]["Energy Usage"]
    filt_power = data["Filtration and Dehydration"][filt]["Energy Usage"]
    dhyd_power = data["Filtration and Dehydration"][dhyd]["Energy Usage"]
    return(ferm_power + dist_power + filt_power + dhyd_power)

results = np.zeros((4, 4, 4, 4), dtype=np.object_)
for ferm in range(4):
    for dist in range(4):
        for filt in range(4):
            for dhyd in range(4):
                results[ferm][dist][filt][dhyd] = result(opsData["Fermenters"][ferm]["Name"], opsData["Distillation Units"][dist]["Name"], opsData["Filtration and Dehydration"][filt]["Name"], opsData["Filtration and Dehydration"][dhyd]["Name"], calculateEff(opsData, ferm, dist, filt, dhyd), calculateCost(opsData, ferm, dist, filt, dhyd), calculatePower(opsData, ferm, dist, filt, dhyd))



# print(np.argmax(results))
# print(results.flatten()[np.argmax(results)])

print(f"{round(time.time() - start, 5)} seconds")