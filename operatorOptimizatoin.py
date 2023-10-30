import json
import numpy as np
import operationCalculations as oC

def loadData(filepath):
    with open(filepath, "r") as file:
        return json.load(file)
    
data = loadData("data/operators.json")
class result:
    def __init__(self, eff=0, cost=0, power=0) -> None:
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
        maxEff = max(self.eff, other.eff)
        minCost = min(self.cost, other.cost)
        minEnergy = min(self.power, other.power)

        selfScore = (self.eff / maxEff) + (self.cost / minCost) + (self.power / minEnergy)
        otherScore = (other.eff / maxEff) + (other.cost / minCost) + (other.power / minEnergy)

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
        return f"eff: {self.eff}, cost: ${self.cost}, energy: {self.power}kW"
    
a = [
    [1, 2, 3, 4],
    [1, 2, 3, 4]
]

b = [
    [11, 12, 13, 14],
    [21, 22, 23, 24],
    [31, 32, 33, 34],
    [41, 42, 43, 44]
]

def calculateEff(data, ferm, dist, filt, dhyd):
    # print(data["Fermenters"][ferm])
    ferm_eff = data["Fermenters"][ferm]["Efficiency"]
    dist_eff = data["Fermenters"][dist]["Efficiency"]
    filt_eff = data["Fermenters"][filt]["Efficiency"]
    dhyd_eff = data["Fermenters"][dhyd]["Efficiency"]
    return(ferm_eff * dist_eff * filt_eff * dhyd_eff)

def calculateCost(data, ferm, dist, filt, dhyd):
    ferm_cost = data["Fermenters"][ferm]["Cost"]
    dist_cost = data["Fermenters"][dist]["Cost"]
    filt_cost = data["Fermenters"][filt]["Cost"]
    dhyd_cost = data["Fermenters"][dhyd]["Cost"]
    return(ferm_cost + dist_cost + filt_cost + dhyd_cost)

def calculatePower(data, ferm, dist, filt, dhyd):
    ferm_power = data["Fermenters"][ferm]["Energy Usage"]
    dist_power = data["Fermenters"][dist]["Energy Usage"]
    filt_power = data["Fermenters"][filt]["Energy Usage"]
    dhyd_power = data["Fermenters"][dhyd]["Energy Usage"]
    return(ferm_power + dist_power + filt_power + dhyd_power)

results = np.zeros((4, 4, 4, 4), dtype=np.object_)

for ferm in range(4):
    for dist in range(4):
        for filt in range(4):
            for dhyd in range(4):
                results[ferm][dist][filt][dhyd] = result(calculateEff(data, ferm, dist, filt, dhyd), calculateCost(data, ferm, dist, filt, dhyd), calculatePower(data, ferm, dist, filt, dhyd))


print(np.argmax(results))
print(results.flatten()[np.argmax(results)])