from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *

class MagicWordManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("MagicWordManagerAI")

    def setMagicWord(self, word, targetId, zoneId):
        clientMagicWords = ['endgame', 'wingame', 'oobe', 'tex', 'wire', 'showfont', 'hidefont',
                            'walk', 'rogues', 'showCS', 'hideCS', 'showCollisions', 'hideCollisions', 
                            'showCameraCollisions', 'hideCameraCollisions', 'listen', 'nochat', 'chat',
                            'superchat', 'stress', 'for', 'badname', 'doId', 'hideAttack', 'showAttack',
                            'collisions_on', 'collisions_off', 'battle_detect_off', 'battle_detect_on',
                            'addCameraPosition', 'removeCameraPosition', 'printCameraPosition', 'printCameraPositions',
                            'magic', 'exec', 'run', 'who', 'period', 'direct', 'tt', 'cogPageFull']
        
        invokerId = self.air.getAvatarIdFromSender()
        invoker = self.air.doId2do.get(invokerId)
        target = self.air.doId2do.get(targetId)
        
        word = word[1:] # Chop off the ~ at the start. It's not needed.
        splitWord = word.split(' ')
        args = splitWord[1:]
        word = splitWord[0].lower()
        del splitWord
        
        for clientWord in clientMagicWords:
            testWord = clientWord.lower()
            if testWord in word or word == testWord:
                self.notify.debug("Avatar %d used Client Magic Word '%s', Arguments were %s" % (invokerId, word, str(args)))
                self.air.writeServerEvent('client-magic-word', invokerId, word, args)
                return
        
        if word == 'sethp':
            try:
                hp = int(args[0])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setHp(hp)
            elif invoker:
                invoker.b_setHp(hp)
        elif word == 'setmaxhp':
            try:
                maxHp = int(args[0])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setMaxHp(maxHp)
            elif invoker:
                invoker.b_setMaxHp(maxHp)
        elif word == 'setmoney':
            try:
                money = int(args[0])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setMoney(money)
            elif invoker:
                invoker.b_setMoney(money)
        elif word == 'setmaxmoney':
            try:
                maxMoney = int(args[0])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setMaxMoney(maxMoney)
            elif invoker:
                invoker.b_setMaxMoney(maxMoney)
        elif word == 'setbankmoney':
            try:
                bankMoney = int(args[0])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setBankMoney(bankMoney)
            elif invoker:
                invoker.b_setBankMoney(bankMoney)
        elif word == 'setmaxbankmoney':
            try:
                maxBankMoney = int(args[0])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setMaxBankMoney(maxBankMoney)
            elif invoker:
                invoker.b_setMaxBankMoney(maxBankMoney)
        elif word == 'name':
            try:
                name = " ".join(str(x) for x in args)
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setName(name)
            elif invoker:
                invoker.b_setName(name)
        elif word == 'setmaxcarry':
            try:
                maxCarry = int(args[0])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setMaxCarry(maxCarry)
            elif invoker:
                invoker.b_setMaxCarry(maxCarry)
        elif invoker:
            self.air.writeServerEvent('invalid-magic-word', invokerId, word)
            self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Magic Word does not exist!"])

    def setWho(self, avIds):
        pass