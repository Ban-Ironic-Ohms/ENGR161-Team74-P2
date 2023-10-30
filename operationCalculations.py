class solution:
    def __init__(self, water, fiber, sugar,ethanol) -> None:
        self.water = water
        self.fiber = fiber
        self.sugar = sugar
        self.ethanol = ethanol

#class waste(solution):
#   def __init__(self) -> None:
#      super().__init__()
#     self.state = solid lq, gas
    
    
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
