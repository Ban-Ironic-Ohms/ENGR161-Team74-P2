class Solution:
    def __init__(self, water, fiber, sugar,ethanol) -> None:
        self.water = water
        self.fiber = fiber
        self.sugar = sugar
        self.ethanol = ethanol

waste = 0 #measured in % mass of original value. 
#class waste(solution):
#   def __init__(self) -> None:
#      super().__init__()
#     self.state = solid lq, gas


def fermenter(eff, sol):
    totalMass = sol.sugar+sol.fiber+sol.water+sol.ethanol * 1
    lostMass = sol.sugar * 0.49
    newMass = totalMass - lostMass
    massSugar = sol.sugar * (1 - eff)
    massFiber = sol.fiber
    massWater = sol.water
    massEthanol = sol.sugar * eff * 0.51
    sol.sugar = massSugar/newMass
    sol.fiber = massFiber/newMass
    sol.Water = massWater/newMass
    sol.Ethanol = massEthanol/newMass
    return sol

def filt(eff, sol):
    sol.sugar = sol.sugar
    sol.fiber = sol.fiber * (1-eff)
    sol.water = sol.water
    sol.ethanol = sol.ethanol
    return sol


def distiller(eff, sol):
    sol.sugar = (sol.sugar * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    sol.fiber = (sol.fiber * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    sol.water = (sol.water * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    sol.ethanol = sol.ethanol
    return sol


def dehydrator(eff, sol):
    sol.sugar = sol.sugar
    sol.fiber = sol.fiber
    sol.water = sol.water * (1-eff)
    sol.ethanol = sol.ethanol
