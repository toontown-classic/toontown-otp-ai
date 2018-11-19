import random

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM

from toontown.safezone import ButterflyGlobals


class DistributedButterflyAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedButterflyAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedButterflyAI')

        self.area = 0
        self.playground = 0
        self.stateIndex = 0
        self.curIndex = 0
        self.destIndex = 0
        self.time = 0
        self.timestamp = 0

        self.__currentTask = None

    def generate(self):
        ButterflyGlobals.generateIndexes(self.doId, self.playground)
        self.request('TakeOff')

    def setArea(self, playground, area):
        self.area = area
        self.playground = playground

    def d_setArea(self, playground, area):
        self.sendUpdate('setArea', [playground, area])

    def b_setArea(self, playground, area):
        self.setArea(playground, area)
        self.d_setArea(playground, area)

    def getArea(self):
        return [self.playground, self.area]

    def setState(self, stateIndex, curIndex, destIndex, time, timestamp):
        self.stateIndex = stateIndex
        self.curIndex = curIndex
        self.destIndex = destIndex
        self.time = time
        self.timestamp = timestamp

    def d_setState(self, stateIndex, curIndex, destIndex, time, timestamp):
        self.sendUpdate('setState', [stateIndex, curIndex, destIndex, time, timestamp])

    def b_setState(self, stateIndex, curIndex, destIndex, time, timestamp):
        self.setState(stateIndex, curIndex, destIndex, time, timestamp)
        self.d_setState(stateIndex, curIndex, destIndex, time, timestamp)

    def getState(self):
        return [self.stateIndex, self.curIndex, self.destIndex, self.time, self.timestamp]

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def __takeOff(self, task):
        self.request('TakeOff')
        return task.done

    def enterTakeOff(self):
        fr = ButterflyGlobals.getFirstRoute(self.playground, self.area, self.doId)
        self.b_setState(ButterflyGlobals.FLYING, fr[1], fr[3], fr[4],
            globalClockDelta.getRealNetworkTime())

        self.__currentTask = taskMgr.doMethodLater(fr[4], self.__land,
            self.uniqueName('landButterfly'))

    def exitTakeOff(self):
        if self.__currentTask:
            taskMgr.remove(self.__currentTask)
            self.__currentTask = None

    def __land(self, task):
        self.request('Land')
        return task.done

    def enterLand(self):
        ttl = random.uniform(0, ButterflyGlobals.MAX_LANDED_TIME)
        self.b_setState(ButterflyGlobals.LANDED, self.curIndex, self.destIndex, ttl,
            globalClockDelta.getRealNetworkTime())

        self.__currentTask = taskMgr.doMethodLater(ttl, self.__fly,
            self.uniqueName('flyButterfly'))

    def exitLand(self):
        if self.__currentTask:
            taskMgr.remove(self.__currentTask)
            self.__currentTask = None

    def __fly(self, task):
        self.request('Fly')
        return task.done

    def enterFly(self):
        nextPos = ButterflyGlobals.getNextPos(ButterflyGlobals.ButterflyPoints[self.playground][
            self.area][self.destIndex], self.playground, self.area, self.doId)

        self.b_setState(ButterflyGlobals.FLYING, self.destIndex, nextPos[1], nextPos[2],
            globalClockDelta.getRealNetworkTime())

        self.__currentTask = taskMgr.doMethodLater(nextPos[2], self.__land,
            self.uniqueName('landButterfly'))

    def exitFly(self):
        if self.__currentTask:
            taskMgr.remove(self.__currentTask)
            self.__currentTask = None

    def avatarEnter(self):
        pass

    def delete(self):
        if self.__currentTask:
            taskMgr.remove(self.__currentTask)
            self.__currentTask = None

        self.cleanup()
        DistributedObjectAI.delete(self)
