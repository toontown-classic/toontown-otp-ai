from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class FriendManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("FriendManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.currentContext = 0
        self.requests = {}
        self.teleportRequests = {}

    def friendQuery(self, requested):
        avId = self.air.getAvatarIdFromSender()
        if not requested in self.air.doId2do:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to friend a player that does not exist!')
            return
        context = self.currentContext
        self.requests[context] = [ [ avId, requested ], 'friendQuery']
        self.currentContext += 1
        self.sendUpdateToAvatarId(requested, 'inviteeFriendQuery', [avId, self.air.doId2do[avId].getName(), self.air.doId2do[avId].getDNAString(), context])

    def cancelFriendQuery(self, context):
        avId = self.air.getAvatarIdFromSender()
        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to cancel a request that doesn\'t exist!')
            return
        if avId != self.requests[context][0][0]:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to cancel someone elses request!')
            return
        self.requests[context][1] = 'cancelled'
        self.sendUpdateToAvatarId(self.requests[context][0][1], 'inviteeCancelFriendQuery', [context])

    def inviteeFriendConsidering(self, yesNo, context):
        avId = self.air.getAvatarIdFromSender()
        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to consider a friend request that doesn\'t exist!')
            return
        if avId != self.requests[context][0][1]:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to consider for someone else!')
            return
        if self.requests[context][1] != 'friendQuery':
            self.air.writeServerEvent('suspicious', avId, 'Player tried to reconsider friend request!')
            return
        if yesNo != 1:
            self.sendUpdateToAvatarId(self.requests[context][0][0], 'friendConsidering', [yesNo, context])
            del self.requests[context]
            return
        self.requests[context][1] = 'friendConsidering'
        self.sendUpdateToAvatarId(self.requests[context][0][0], 'friendConsidering', [yesNo, context])

    def inviteeFriendResponse(self, response, context):
        avId = self.air.getAvatarIdFromSender()
        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to respond to a friend request that doesn\'t exist!')
            return
        if avId != self.requests[context][0][1]:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to respond to someone else\'s request!')
            return
        if self.requests[context][1] == 'cancelled':
            self.air.writeServerEvent('suspicious', avId, 'Player tried to respond to non-active friend request!')
            return
        self.sendUpdateToAvatarId(self.requests[context][0][0], 'friendResponse', [response, context])
        if response == 1:

            requested = self.requests[context][0][1]
            if requested in self.air.doId2do:
                requested = self.air.doId2do[requested]
            else:
                del self.requests[context]
                return

            requester = self.requests[context][0][0]
            if requester in self.air.doId2do:
                requester = self.air.doId2do[requester]
            else:
                del self.requests[context]
                return

            requested.extendFriendsList(requester.getDoId(), 0)
            requester.extendFriendsList(requested.getDoId(), 0)

            requested.d_setFriendsList(requested.getFriendsList())
            requester.d_setFriendsList(requester.getFriendsList())
        del self.requests[context]


    def inviteeAcknowledgeCancel(self, context):
        avId = self.air.getAvatarIdFromSender()
        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to acknowledge the cancel of a friend request that doesn\'t exist!')
            return
        if avId != self.requests[context][0][1]:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to acknowledge someone else\'s cancel!')
            return
        if self.requests[context][1] != 'cancelled':
            self.air.writeServerEvent('suspicious', avId, 'Player tried to cancel non-cancelled request!')
            return
        del self.requests[context]

    def requestSecret(self):
        pass

    def submitSecret(self, todo0):
        pass

    def teleportQuery(self, fromAvId, toAvId):
        if fromAvId in self.teleportRequests:
            return

        dclass = self.air.dclassesByName['DistributedToonAI']
        dg = dclass.aiFormatUpdate('teleportQuery', toAvId, self.GetPuppetConnectionChannel(toAvId), fromAvId, [fromAvId])
        self.air.send(dg)

        self.teleportRequests[fromAvId] = toAvId
        taskMgr.doMethodLater(5, self.giveUpTeleportQuery, 'tp-query-timeout-%d' % fromAvId, extraArgs=[fromAvId, toAvId])

    def giveUpTeleportQuery(self, fromAvId, toAvId):
        if fromAvId not in self.teleportRequests:
            return

        dclass = self.air.dclassesByName['DistributedToonAI']
        dg = dclass.aiFormatUpdate('teleportResponse', fromAvId, self.GetPuppetConnectionChannel(fromAvId), toAvId, [toAvId,
            0, 0, 0, 0])

        self.air.send(dg)

        del self.teleportRequests[fromAvId]
        self.notify.warning('Teleport request that was sent by %d to %d timed out.' % (fromAvId, toAvId))

    def teleportResponse(self, fromAvId, toAvId, available, shardId, hoodId, zoneId):
        if fromAvId not in self.teleportRequests:
            return

        if taskMgr.hasTaskNamed('tp-query-timeout-%d' % fromAvId):
            taskMgr.remove('tp-query-timeout-%d' % fromAvId)

        dclass = self.air.dclassesByName['DistributedToonAI']
        dg = dclass.aiFormatUpdate('teleportResponse', fromAvId, self.GetPuppetConnectionChannel(fromAvId), toAvId, [toAvId,
            available, shardId, hoodId, zoneId])

        self.air.send(dg)

        del self.teleportRequests[fromAvId]
