from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *

class MagicWordManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("MagicWordManagerAI")

    def setMagicWord(self, word, targetId, zoneId):
        invokerId = self.air.getAvatarIdFromSender()
        invoker = self.air.doId2do.get(invokerId)
        target = self.air.doId2do.get(targetId)
        
        word = word[1:] # Chop off the ~ at the start. It's not needed.
        
        if word[:5].lower() == 'sethp':
            try:
                hp = int(word[5:])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setHp(hp)
            elif invoker:
                invoker.b_setHp(hp)
        elif word[:8].lower() == 'setmaxhp':
            try:
                maxHp = int(word[8:])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setMaxHp(maxHp)
            elif invoker:
                invoker.b_setMaxHp(maxHp)
        elif word[:8].lower() == 'setmoney':
            try:
                money = int(word[8:])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setMoney(money)
            elif invoker:
                invoker.b_setMoney(money)
        elif word[:11].lower() == 'setmaxmoney':
            try:
                maxMoney = int(word[11:])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setMaxMoney(maxMoney)
            elif invoker:
                invoker.b_setMaxMoney(maxMoney)
        elif word[:12].lower() == 'setbankmoney':
            try:
                bankMoney = int(word[12:])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setBankMoney(bankMoney)
            elif invoker:
                invoker.b_setBankMoney(bankMoney)
        elif word[:15].lower() == 'setmaxbankmoney':
            try:
                maxBankMoney = int(word[15:])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setMaxBankMoney(maxBankMoney)
            elif invoker:
                invoker.b_setMaxBankMoney(maxBankMoney)
        elif word[:4].lower() == 'name':
            try:
                name = str(word[5:])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setName(name)
            elif invoker:
                invoker.b_setName(name)
        elif word[:11].lower() == 'setmaxcarry':
            try:
                maxCarry = int(word[11:])
            except:
                if invoker:
                    self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Invalid arguments for Magic Word!"])
                return

            if target:
                target.b_setMaxCarry(maxCarry)
            elif invoker:
                invoker.b_setMaxCarry(maxCarry)
        elif invoker:
            self.sendUpdateToAvatarId(invokerId, 'setMagicWordResponse', ["Magic Word does not exist!"])

    def setWho(self, avIds):
        pass