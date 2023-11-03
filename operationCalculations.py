class Solution:
    def __init__(self, initialMFR) -> None:
        """
        Initilizer
        
        Args:
            initialMFR (float): the mass flow rate in m^3/h of the initial solution
        """
        self.water = initialMFR * 0.6 # in m^3 / h
        self.fiber = initialMFR * 0.2 # in m^3 / h
        self.sugar = initialMFR * 0.2 # in m^3 / h
        self.ethanol = 0 # in m^3 / h
        
        # print(self)
        
    def massFlowRate(self):
        return sum([self.water, self.fiber, self.sugar, self.ethanol])

    # using aproximation outlined in slides
    def density(self):
        density = 0
        mass = self.massFlowRate()
        density += (self.water / mass) * 998 # from https://www.usgs.gov/special-topics/water-science-school/science/water-density at 70F
        density += (self.fiber / mass) * 381 # from https://www.aqua-calc.com/page/density-table/substance/all-blank-bran-coma-and-blank-a-blank-wheat-blank-bran-blank-fiber-blank-cereal-coma-and-blank-upc-column--blank-038000013027
        density += (self.sugar / mass) * 1552 # from https://wiki.anton-paar.com/us-en/density-and-density-measurement/sucrose-density/
        density += (self.ethanol / mass) * 779 # from https://pubchem.ncbi.nlm.nih.gov/compound/Ethanol#section=Experimental-Properties
        
        return density
    
    def __str__(self) -> str:
        return f"{self.water:.4f}m^3/h water, {self.fiber:.4f}m^3/h fiber, {self.sugar:.4f}m^3/h sugar, {self.ethanol:.4f}m^3/h ethanol with total mass {self.massFlowRate():.4f} and density {self.density():.4f}"

    def ethanolConcentration(self):
        return self.ethanol / self.massFlowRate()

waste = 0 #measured in % mass of original value. 
#class waste(solution):
#   def __init__(self) -> None:
#      super().__init__()
#     self.state = solid lq, gas

# TODO for Mitch -- change these so that they work DIRECTLY with masses
# this is an example -- we dont need lostMass, and dont need to divide by
# 'newMass' 
def fermenter(eff, sol):
    sol.ethanol += sol.sugar * eff * 0.51 # also note that with this implimentation, the ethanol math needs to happen first otherwise the ethanol will be based off reduced sugar
    sol.sugar = sol.sugar * (1 - eff)
    sol.fiber = sol.fiber
    sol.water = sol.water
    return sol

def filt(eff, sol):
    sol.sugar = sol.sugar
    sol.water = sol.water
    sol.ethanol = sol.ethanol
    sol.fiber = sol.fiber * (1 - eff)
    
    # totalMass = sol.sugar + sol.fiber + sol.water + sol.ethanol * 1
    # lostMass =  sol.fiber * eff
    # newMass = totalMass - lostMass
    # massSugar = sol.sugar
    # massFiber = sol.fiber * (1-eff)
    # massWater = sol.water
    # massEthanol = sol.ethanol
    # sol.sugar = massSugar/newMass
    # sol.fiber = massFiber/newMass
    # sol.water = massWater/newMass
    # sol.ethanol = massEthanol/newMass
    return sol


def distiller(eff, sol):
    # totalMass = sol.sugar + sol.fiber + sol.water + sol.ethanol * 1
    
    sol.sugar = (sol.sugar * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    sol.fiber = (sol.fiber * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    sol.water = (sol.water * sol.ethanol * ((1/eff)-1))/(sol.water + sol.ethanol + sol.fiber)
    sol.ethanol = sol.ethanol
    
    # lostMass = (sol.fiber - massFiber)+(sol.sugar - massSugar)+(sol.water-massWater)
    # newMass = totalMass - lostMass
    
    # sol.sugar = massSugar/newMass
    # sol.fiber = massFiber/newMass
    # sol.water = massWater/newMass
    # sol.ethanol = massEthanol/newMass
    return sol


def dehydrator(eff, sol):
    # totalMass = sol.sugar + sol.fiber + sol.water + sol.ethanol * 1
    # lostMass = sol.water * eff
    # newMass = totalMass - lostMass
    sol.sugar = sol.sugar
    sol.fiber = sol.fiber
    sol.water = sol.water * (1-eff)
    sol.ethanol = sol.ethanol
    # sol.sugar = massSugar/newMass
    # sol.fiber = massFiber/newMass
    # sol.water = massWater/newMass
    # sol.ethanol = massEthanol/newMass
    return sol

