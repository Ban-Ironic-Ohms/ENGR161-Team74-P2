#This is the solution, contianing the percent mass of the parts of the solution that make up it.
class Solution:
    def __init__(self, water, fiber, sugar,ethanol) -> None:
        self.water = water
        self.fiber = fiber
        self.sugar = sugar
        self.ethanol = ethanol

#class waste(solution):
#   def __init__(self) -> None:
#      super().__init__()
#     self.state = solid lq, gas

#This takes in the efficiency of the fermenter, and outputs the new solution.
def fermenter(eff, sol):
    sol.sugar = sol.sugar * (1 - eff)
    sol.fiber = sol.fiber
    sol.water = sol.water
    sol.ethanol = sol.sugar * eff
    return sol

def filter(eff, sol):
    sol.sugar = sol.sugar
    sol.fiber = sol.fiber * (1-eff)
    sol.water = sol.water
    sol.ethanol = sol.ethanol
    return sol

#This takes in the efficiency of the distiller, and outputs the new solution.
def distiller(eff, sol):
    sol.sugar = (sol.sugar * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    sol.fiber = (sol.fiber * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    sol.water = (sol.water * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    sol.ethanol = sol.ethanol
    return sol

#This takes in the efficiency of the dehydrator, and outputs the new solution.
def dehydrator(eff, sol):
    sol.sugar = sol.sugar
    sol.fiber = sol.fiber
    sol.water = sol.water * (1-eff)
    sol.ethanol = sol.ethanol
