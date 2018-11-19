from toontown.safezone.DistributedTreasure import DistributedTreasure
from direct.directnotify import DirectNotifyGlobal

class DistributedTagTreasure(DistributedTreasure):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTagTreasure')

    def __init__(self, cr):
        DistributedTreasure.__init__(self, cr)
