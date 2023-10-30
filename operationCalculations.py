class solution:
    def __init__(self, water, fiber, sugar,ethanol) -> None:
        self.water = water
        self.fiber = fiber
        self.sugar = sugar
        self.ethanol = ethanol

class waste(solution):
    def __init__(self) -> None:
        super().__init__()
        self.state = solid lq, gas
    
    
def fermenter(eff, sol):
    sol.sugar = sol.sugar * (1 - eff)
    sol.fiber = sol.fiber
    sol.water = sol.water
    sol.ethanol = sol.sugar * eff
    return sol

def filter(eff, sol):
    