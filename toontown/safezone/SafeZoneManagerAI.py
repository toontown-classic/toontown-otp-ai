from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed import DistributedObjectAI
from toontown.toon.DistributedToonAI import DistributedToonAI


HealFrequency = 10.0  # The time in seconds between each Toon-up pulse.


class SafeZoneManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = directNotify.newCategory('SafeZoneManagerAI')

    def enterSafeZone(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av or not isinstance(av, DistributedToonAI):
            return
        av.startToonUp(HealFrequency)

    def exitSafeZone(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av or not isinstance(av, DistributedToonAI):
            return
        av.stopToonUp()
