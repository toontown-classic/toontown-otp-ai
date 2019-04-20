import copy
import random
import time

import DistributedMinigameAI
import DistributedCannonGameAI
import DistributedCatchGameAI
import DistributedCogThiefGameAI
import DistributedDivingGameAI
import DistributedIceGameAI
import DistributedMazeGameAI
import DistributedMinigameTemplateAI
import DistributedPairingGameAI
import DistributedPatternGameAI
import DistributedPhotoGameAI
import DistributedRaceGameAI
import DistributedRingGameAI
import DistributedTagGameAI
import DistributedTargetGameAI
import DistributedTravelGameAI
import DistributedTugOfWarGameAI
import DistributedTwoDGameAI
import DistributedVineGameAI
import TravelGameGlobals
from toontown.minigame.TempMinigameAI import *
from toontown.toonbase import ToontownGlobals


simbase.forcedMinigameId = simbase.config.GetInt('force-minigame', 0)
RequestMinigame = {}
MinigameZoneRefs = {}
DisabledMinigames = []


def getDisabledMinigames():
    if not DisabledMinigames:
        for name, minigameId in ToontownGlobals.MinigameNames.items():
            if not simbase.config.GetBool('want-%s-game' % name, True):
                if minigameId not in DisabledMinigames:
                    DisabledMinigames.append(minigameId)
    return DisabledMinigames[:]


def createMinigame(air, playerArray, trolleyZone, minigameZone=None,
        previousGameId=ToontownGlobals.NoPreviousGameId, newbieIds=[],
        startingVotes=None, metagameRound=-1, desiredNextGame=None):
    if minigameZone is None:
        minigameZone = air.allocateZone()
    acquireMinigameZone(minigameZone)
    mgId = None
    mgDiff = None
    mgSzId = None
    for avId in playerArray:
        request = RequestMinigame.get(avId)
        if request is not None:
            mgId, mgKeep, mgDiff, mgSzId = request
            if not mgKeep:
                del RequestMinigame[avId]
            break
    if mgId is not None:
        pass
    elif simbase.forcedMinigameId:
        mgId = simbase.forcedMinigameId
    else:
        #randomList = list(copy.copy(ToontownGlobals.MinigamePlayerMatrix[len(playerArray)]))
        #if len(playerArray) > 1:
        #    randomList = list(copy.copy(ToontownGlobals.MinigameIDs))
        randomList = [
            ToontownGlobals.CannonGameId,
            ToontownGlobals.PatternGameId,
            ToontownGlobals.TugOfWarGameId
        ]
        if len(playerArray) > 1:
            randomList = list(randomList)
            randomList.append(ToontownGlobals.TagGameId)

        #for gameId in [ToontownGlobals.TravelGameId] + getDisabledMinigames():
        #    if gameId in randomList:
        #        randomList.remove(gameId)
        #if previousGameId != ToontownGlobals.NoPreviousGameId:
        #    if randomList.count(previousGameId) != 0 and len(randomList) > 1:
        #        randomList.remove(previousGameId)
        mgId = random.choice(randomList)
        #if metagameRound > -1:
        #    if (metagameRound%2) == 0:
        #        mgId = ToontownGlobals.TravelGameId
        #    if desiredNextGame:
        #        mgId = desiredNextGame

    mgCtors = {
        ToontownGlobals.RaceGameId: DistributedRaceGameAI.DistributedRaceGameAI,
        ToontownGlobals.CannonGameId: DistributedCannonGameAI.DistributedCannonGameAI,
        ToontownGlobals.TagGameId: DistributedTagGameAI.DistributedTagGameAI,
        ToontownGlobals.PatternGameId: DistributedPatternGameAI.DistributedPatternGameAI,
        ToontownGlobals.RingGameId: DistributedRingGameAI.DistributedRingGameAI,
        ToontownGlobals.MazeGameId: DistributedMazeGameAI.DistributedMazeGameAI,
        ToontownGlobals.TugOfWarGameId: DistributedTugOfWarGameAI.DistributedTugOfWarGameAI,
        ToontownGlobals.CatchGameId: DistributedCatchGameAI.DistributedCatchGameAI,
    }
    from TempMinigameAI import TempMgCtors
    for key, value in TempMgCtors.items():
        mgCtors[key] = value
    try:
        mg = mgCtors[mgId](air, mgId)
    except Exception as e:
        raise (e)
    mg.setExpectedAvatars(playerArray)
    mg.setNewbieIds(newbieIds)
    mg.setTrolleyZone(trolleyZone)
    mg.setDifficultyOverrides(mgDiff, mgSzId)
    if startingVotes == None:
        for avId in playerArray:
            mg.setStartingVote(avId, TravelGameGlobals.DefaultStartingVotes)
    else:
        for index in xrange(len(startingVotes)):
            avId = playerArray[index]
            votes = startingVotes[index]
            if votes < 0:
                print 'createMinigame negative votes, avId=%s votes=%s' % (avId, votes)
                votes = 0
            mg.setStartingVote(avId, votes)
    mg.setMetagameRound(metagameRound)
    mg.generateWithRequired(minigameZone)
    toons = []
    for doId in playerArray:
        toon = simbase.air.doId2do.get(doId)
        if toon is not None:
            toons.append(toon)
    for toon in toons:
        simbase.air.questManager.toonPlayedMinigame(toon, toons)
    retVal = {}
    retVal['minigameZone'] = minigameZone
    retVal['minigameId'] = mgId
    return retVal


def acquireMinigameZone(zoneId):
    if zoneId not in MinigameZoneRefs:
        MinigameZoneRefs[zoneId] = 0
    MinigameZoneRefs[zoneId] += 1


def releaseMinigameZone(zoneId):
    MinigameZoneRefs[zoneId] -= 1
    if MinigameZoneRefs[zoneId] <= 0:
        del MinigameZoneRefs[zoneId]
        simbase.air.deallocateZone(zoneId)
