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
    print(data["Fermenters"][ferm])
    ferm_eff = data["Fermenters"][ferm]["Efficiency"]
    dist_eff = data["Fermenters"][dist]["Efficiency"]
    filt_eff = data["Fermenters"][filt]["Efficiency"]
    dhyd_eff = data["Fermenters"][dhyd]["Efficiency"]
    return(ferm_eff * dist_eff * filt_eff * dhyd_eff)

print(calculateEff(data, 1, 1, 1, 1))
    
