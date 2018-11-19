from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
import HouseGlobals
import time

from toontown.safezone.SZTreasurePlannerAI import SZTreasurePlannerAI
from toontown.safezone import TreasureGlobals

class DistributedEstateAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedEstateAI")
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.toons = [0, 0, 0, 0, 0, 0]
        self.houses = [None] * 6
        self.decorData = []
        self.estateType = 0 # NOT SURE IF THIS HAS ANY USE BUT THANKS DISNEY
        
        self.owner = None
        
    def generate(self):
        DistributedObjectAI.generate(self)

        #self.createTreasurePlanner()

    def destroy(self):
        for house in self.houses:
            if house:
                house.requestDelete()
        del self.houses[:]

        '''if self.treasurePlanner:
            self.treasurePlanner.stop()'''

        self.requestDelete()

    def setEstateReady(self):
        pass

    def setClientReady(self):
        self.sendUpdate('setEstateReady', [])

    def setEstateType(self, type):
        self.estateType = type
        
    def d_setEstateType(self, type):
        self.sendUpdate('setEstateType', [type])
        
    def b_setEstateType(self, type):
        self.setEstateType(type)
        self.d_setEstateType(type)

    def getEstateType(self):
        return self.estateType
        
    def setClosestHouse(self, todo0):
        pass

    def setTreasureIds(self, todo0):
        pass
        
    def createTreasurePlanner(self):
        treasureType, healAmount, spawnPoints, spawnRate, maxTreasures = TreasureGlobals.SafeZoneTreasureSpawns[ToontownGlobals.MyEstate]
        self.treasurePlanner = SZTreasurePlannerAI(self.zoneId, treasureType, healAmount, spawnPoints, spawnRate, maxTreasures)
        self.treasurePlanner.start()