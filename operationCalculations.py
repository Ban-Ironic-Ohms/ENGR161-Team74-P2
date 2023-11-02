class Solution:
    def __init__(self, initialMass) -> None:
        self.water = initialMass * 0.6 # in kg
        self.fiber = initialMass * 0.2 # in kg
        self.sugar = initialMass * 0.2 # in kg
        self.ethanol = 0 # in kg
        
    def mass(self):
        return sum([self.water, self.fiber, self.sugar, self.ethanol])

    # using aproximation outlined in slides
    def density(self):
        density = 0
        mass = self.mass()
        density += (self.water / mass) * 998 # from https://www.usgs.gov/special-topics/water-science-school/science/water-density at 70F
        density += (self.fiber / mass) * 381 # from https://www.aqua-calc.com/page/density-table/substance/all-blank-bran-coma-and-blank-a-blank-wheat-blank-bran-blank-fiber-blank-cereal-coma-and-blank-upc-column--blank-038000013027
        density += (self.sugar / mass) * 1552 # from https://wiki.anton-paar.com/us-en/density-and-density-measurement/sucrose-density/
        density += (self.ethanol / mass) * 779 # from https://pubchem.ncbi.nlm.nih.gov/compound/Ethanol#section=Experimental-Properties
        

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
    totalMass = sol.sugar + sol.fiber + sol.water + sol.ethanol * 1
    lostMass =  sol.fiber * eff
    newMass = totalMass - lostMass
    massSugar = sol.sugar
    massFiber = sol.fiber * (1-eff)
    massWater = sol.water
    massEthanol = sol.ethanol
    sol.sugar = massSugar/newMass
    sol.fiber = massFiber/newMass
    sol.Water = massWater/newMass
    sol.Ethanol = massEthanol/newMass
    return sol


def distiller(eff, sol):
    totalMass = sol.sugar + sol.fiber + sol.water + sol.ethanol * 1
    massSugar = (sol.sugar * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    massFiber = (sol.fiber * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    massWater = (sol.water * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    massEthanol = sol.ethanol
    lostMass = (sol.fiber - massFiber)+(sol.sugar - massSugar)+(sol.water-massWater)
    newMass = totalMass - lostMass
    sol.sugar = massSugar/newMass
    sol.fiber = massFiber/newMass
    sol.Water = massWater/newMass
    sol.Ethanol = massEthanol/newMass
    return sol


def dehydrator(eff, sol):
    totalMass = sol.sugar + sol.fiber + sol.water + sol.ethanol * 1
    lostMass = sol.water * eff
    newMass = totalMass - lostMass
    massSugar = sol.sugar
    massFiber = sol.fiber
    massWater = sol.water * (1-eff)
    massEthanol = sol.ethanol
    sol.sugar = massSugar/newMass
    sol.fiber = massFiber/newMass
    sol.Water = massWater/newMass
    sol.Ethanol = massEthanol/newMass
    return sol

