class Solution:
    def __init__(self, initialVFR) -> None:
        """
        Initilizer
        
        Args:
            initialVFR (float): the volume flow rate in m^3/h of the initial solution
        """
        
        self.waterDensity = 998 # from https://www.usgs.gov/special-topics/water-science-school/science/water-density at 70F
        self.fiberDensity = 381 # from https://www.aqua-calc.com/page/density-table/substance/all-blank-bran-coma-and-blank-a-blank-wheat-blank-bran-blank-fiber-blank-cereal-coma-and-blank-upc-column--blank-038000013027
        self.sugarDensity = 1552 # from https://wiki.anton-paar.com/us-en/density-and-density-measurement/sucrose-density/
        self.ethanolDensity = 779 # from https://pubchem.ncbi.nlm.nih.gov/compound/Ethanol#section=Experimental-Properties
        
        oneOverSum = 1 / ( (0.6 / self.waterDensity) + (0.2 / self.fiberDensity) + (0.2 / self.sugarDensity))
        
        self.ethanol = 0 
        self.water = initialVFR * (oneOverSum) * (0.6 / self.waterDensity) 
        self.fiber = initialVFR * (oneOverSum) * (0.2 / self.fiberDensity)
        self.sugar = initialVFR * (oneOverSum) * (0.2 / self.sugarDensity) 
         
        
        # print(self)
    
    @property
    def waterMFR(self):
        return self.water * self.waterDensity
    
    @waterMFR.setter
    def waterMFR(self, MFR):
        self.water = MFR / self.waterDensity
    
    @property
    def fiberMFR(self):
        return self.fiber * self.fiberDensity
    
    @fiberMFR.setter
    def fiberMFR(self, MFR):
        self.fiber = MFR / self.fiberDensity
    
    @property
    def sugarMFR(self):
        return self.sugar * self.sugarDensity
    
    @sugarMFR.setter
    def sugarMFR(self, MFR):
        self.sugar = MFR / self.sugarDensity
    
    @property
    def ethanolMFR(self):
        return self.ethanol * self.ethanolDensity
    
    @ethanolMFR.setter
    def ethanolMFR(self, MFR):
        self.ethanol = MFR / self.ethanolDensity
    
    def volumeFlowRate(self):
        return self.water + self.fiber + self.sugar + self.ethanol
    
    def massFlowRate(self):
        return self.waterMFR + self.fiberMFR + self.sugarMFR + self.ethanolMFR

    # using aproximation outlined in slides
    def density(self):
        density = 0
        mass = self.volumeFlowRate()
        density += (self.water / mass) * self.waterDensity
        density += (self.fiber / mass) * self.fiberDensity
        density += (self.sugar / mass) * self.sugarDensity
        density += (self.ethanol / mass) * self.ethanolDensity
        
        return density
    
    def __str__(self) -> str:
        return f"{self.water:.4f}m^3/h water, {self.fiber:.4f}m^3/h fiber, {self.sugar:.4f}m^3/h sugar, {self.ethanol:.4f}m^3/h ethanol with total volume flow rate {self.volumeFlowRate():.4f} m^3/h and density {self.density():.4f}"

    def ethanolConcentration(self):
        return self.ethanol / self.volumeFlowRate()

waste = 0 #measured in % mass of original value. 
#class waste(solution):
#   def __init__(self) -> None:
#      super().__init__()
#     self.state = solid lq, gas


def fermenter(eff, sol):
    sol.ethanolMFR += sol.sugarMFR * eff * 0.51 # also note that with this implimentation, the ethanol math needs to happen first otherwise the ethanol will be based off reduced sugar
    sol.sugarMFR = sol.sugarMFR * (1 - eff)
    sol.fiberMFR = sol.fiberMFR
    sol.waterMFR = sol.waterMFR
    return sol

def filt(eff, sol):
    sol.sugarMFR = sol.sugarMFR
    sol.waterMFR = sol.waterMFR
    sol.ethanolMFR = sol.ethanolMFR
    sol.fiberMFR = sol.fiberMFR * (1 - eff)
    
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
    
    sol.sugarMFR = (sol.sugarMFR * sol.ethanolMFR * ((1/eff)-1))/(sol.waterMFR + sol.ethanolMFR + sol.fiberMFR)
    sol.fiberMFR = (sol.fiberMFR * sol.ethanolMFR * ((1/eff)-1))/(sol.waterMFR + sol.ethanolMFR + sol.fiberMFR)
    sol.waterMFR = (sol.waterMFR * sol.ethanolMFR * ((1/eff)-1))/(sol.waterMFR + sol.ethanolMFR + sol.fiberMFR)
    sol.ethanolMFR = sol.ethanolMFR
    
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
    sol.sugarMFR = sol.sugarMFR
    sol.fiberMFR = sol.fiberMFR
    sol.waterMFR = sol.waterMFR * (1-eff)
    sol.ethanolMFR = sol.ethanolMFR
    # sol.sugar = massSugar/newMass
    # sol.fiber = massFiber/newMass
    # sol.water = massWater/newMass
    # sol.ethanol = massEthanol/newMass
    return sol

