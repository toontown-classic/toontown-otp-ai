from direct.distributed.PyDatagram import *
from pandac.PandaModules import *
from otp.ai.AIZoneData import AIZoneDataStore
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordManagerAI import MagicWordManagerAI
from otp.ai.TimeManagerAI import TimeManagerAI
from otp.ai import BanManagerAI
from otp.distributed.OtpDoGlobals import *
from toontown.ai.MessageTypes import *
from otp.friends.FriendManagerAI import FriendManagerAI
from toontown.ai import CogPageManagerAI
from toontown.ai import CogSuitManagerAI
from toontown.ai import PromotionManagerAI
from toontown.ai.AchievementsManagerAI import AchievementsManagerAI
from toontown.ai.FishManagerAI import  FishManagerAI
from toontown.ai.HolidayManagerAI import HolidayManagerAI
from toontown.ai.NewsManagerAI import NewsManagerAI
from toontown.ai.QuestManagerAI import QuestManagerAI
from toontown.ai import BankManagerAI
from toontown.building.DistributedTrophyMgrAI import DistributedTrophyMgrAI
from toontown.catalog.CatalogManagerAI import CatalogManagerAI
from toontown.catalog.PopularItemManagerAI import PopularItemManagerAI
from toontown.coghq import CountryClubManagerAI
from toontown.coghq import FactoryManagerAI
from toontown.coghq import LawOfficeManagerAI
from toontown.coghq import MintManagerAI
from toontown.distributed.ToontownDistrictAI import ToontownDistrictAI
from toontown.distributed.ToontownDistrictStatsAI import ToontownDistrictStatsAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from toontown.dna.DNAParser import loadDNAFileAI
from toontown.estate.EstateManagerAI import EstateManagerAI
from toontown.hood import BRHoodAI
from toontown.hood import BossbotHQAI
from toontown.hood import CashbotHQAI
from toontown.hood import DDHoodAI
from toontown.hood import DGHoodAI
from toontown.hood import DLHoodAI
from toontown.hood import GSHoodAI
from toontown.hood import GZHoodAI
from toontown.hood import LawbotHQAI
from toontown.hood import MMHoodAI
from toontown.hood import OZHoodAI
from toontown.hood import SellbotHQAI
from toontown.hood import TTHoodAI
from toontown.hood import ZoneUtil
from toontown.pets.PetManagerAI import PetManagerAI
from toontown.safezone.SafeZoneManagerAI import SafeZoneManagerAI
from toontown.suit.SuitInvasionManagerAI import SuitInvasionManagerAI
from toontown.toon import NPCToons
from toontown.toonbase import ToontownGlobals
from toontown.tutorial.TutorialManagerAI import TutorialManagerAI
from toontown.uberdog.DistributedPartyManagerAI import DistributedPartyManagerAI


class ToontownAIRepository(ToontownInternalRepository):

    def __init__(self, baseChannel, stateServerChannel, districtName):
        ToontownInternalRepository.__init__(
            self, baseChannel, stateServerChannel, dcSuffix='AI')

        self.districtName = districtName
        self.districtPopulation = 0

        self.notify.setInfo(True) # Our AI repository should always log info.
        self.hoods = []
        self.cogHeadquarters = []
        self.dnaStoreMap = {}
        self.dnaDataMap = {}
        self.suitPlanners = {}
        self.buildingManagers = {}
        self.factoryMgr = None
        self.mintMgr = None
        self.lawOfficeMgr = None
        self.countryClubMgr = None

        self.zoneAllocator = UniqueIdAllocator(ToontownGlobals.DynamicZonesBegin,
            ToontownGlobals.DynamicZonesEnd)

        self.zoneDataStore = AIZoneDataStore()

        self.wantFishing = self.config.GetBool('want-fishing', True)
        self.wantHousing = self.config.GetBool('want-housing', True)
        self.wantPets = self.config.GetBool('want-pets', True)
        self.wantParties = self.config.GetBool('want-parties', True)
        self.wantCogbuildings = self.config.GetBool('want-cogbuildings', True)
        self.wantCogdominiums = self.config.GetBool('want-cogdominiums', True)
        self.doLiveUpdates = self.config.GetBool('want-live-updates', False)
        self.wantTrackClsends = self.config.GetBool('want-track-clsends', False)
        self.wantAchievements = self.config.GetBool('want-achievements', True)
        self.wantYinYang = self.config.GetBool('want-yin-yang', False)
        self.baseXpMultiplier = self.config.GetFloat('base-xp-multiplier', 1.0)
        self.wantHalloween = self.config.GetBool('want-halloween', False)
        self.wantChristmas = self.config.GetBool('want-christmas', False)

        self.cogSuitMessageSent = False

    def createManagers(self):
        self.timeManager = TimeManagerAI(self)
        self.timeManager.generateWithRequired(OTP_ZONE_ID_OLD_QUIET_ZONE)
        self.magicWordManager = MagicWordManagerAI(self)
        self.magicWordManager.generateWithRequired(OTP_ZONE_ID_OLD_QUIET_ZONE)
        #self.newsManager = NewsManagerAI(self)
        #self.newsManager.generateWithRequired(2)
        self.safeZoneManager = SafeZoneManagerAI(self)
        self.safeZoneManager.generateWithRequired(OTP_ZONE_ID_OLD_QUIET_ZONE)
        self.tutorialManager = TutorialManagerAI(self)
        #self.tutorialManager.generateWithRequired(2)
        self.friendManager = FriendManagerAI(self)
        self.friendManager.generateWithRequired(OTP_ZONE_ID_OLD_QUIET_ZONE)
        self.questManager = QuestManagerAI(self)
        #self.banManager = BanManagerAI.BanManagerAI(self)
        #self.achievementsManager = AchievementsManagerAI(self)
        self.suitInvasionManager = SuitInvasionManagerAI(self)
        self.trophyMgr = DistributedTrophyMgrAI(self)
        self.trophyMgr.generateWithRequired(OTP_ZONE_ID_OLD_QUIET_ZONE)
        #self.cogSuitMgr = CogSuitManagerAI.CogSuitManagerAI(self)
        #self.promotionMgr = PromotionManagerAI.PromotionManagerAI(self)
        self.cogPageManager = CogPageManagerAI.CogPageManagerAI()
        #self.bankManager = BankManagerAI.BankManagerAI(self)
        self.holidayManager = HolidayManagerAI(self)
        #if self.wantFishing:
        #    self.fishManager = FishManagerAI(self)
        if self.wantHousing:
            self.estateManager = EstateManagerAI(self)
            self.estateManager.generateWithRequired(OTP_ZONE_ID_OLD_QUIET_ZONE)
        #    self.catalogManager = CatalogManagerAI(self)
        #    self.catalogManager.generateWithRequired(2)
        #    self.popularItemManager = PopularItemManagerAI(self)
        #    self.deliveryManager = self.generateGlobalObject(
        #        OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER, 'DistributedDeliveryManager')
        #if self.wantPets:
        #    self.petMgr = PetManagerAI(self)
        #if self.wantParties:
        #    self.partyManager = DistributedPartyManagerAI(self)
        #    self.partyManager.generateWithRequired(2)
        #    self.globalPartyMgr = self.generateGlobalObject(
        #        OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')

    def createSafeZones(self):
        NPCToons.generateZone2NpcDict()
        if self.config.GetBool('want-toontown-central', True):
            self.hoods.append(TTHoodAI.TTHoodAI(self))
        if self.config.GetBool('want-donalds-dock', True):
            self.hoods.append(DDHoodAI.DDHoodAI(self))
        if self.config.GetBool('want-daisys-garden', True):
            self.hoods.append(DGHoodAI.DGHoodAI(self))
        if self.config.GetBool('want-minnies-melodyland', True):
            self.hoods.append(MMHoodAI.MMHoodAI(self))
        if self.config.GetBool('want-the-burrrgh', True):
            self.hoods.append(BRHoodAI.BRHoodAI(self))
        if self.config.GetBool('want-donalds-dreamland', True):
            self.hoods.append(DLHoodAI.DLHoodAI(self))

    def createCogHeadquarters(self):
        NPCToons.generateZone2NpcDict()
        #if self.config.GetBool('want-sellbot-headquarters', True):
        #    self.factoryMgr = FactoryManagerAI.FactoryManagerAI(self)
        #    self.cogHeadquarters.append(SellbotHQAI.SellbotHQAI(self))
        #if self.config.GetBool('want-cashbot-headquarters', True):
        #    self.mintMgr = MintManagerAI.MintManagerAI(self)
        #    self.cogHeadquarters.append(CashbotHQAI.CashbotHQAI(self))
        #if self.config.GetBool('want-lawbot-headquarters', True):
        #    self.lawOfficeMgr = LawOfficeManagerAI.LawOfficeManagerAI(self)
        #    self.cogHeadquarters.append(LawbotHQAI.LawbotHQAI(self))
        #if self.config.GetBool('want-bossbot-headquarters', True):
        #    self.countryClubMgr = CountryClubManagerAI.CountryClubManagerAI(self)
        #    self.cogHeadquarters.append(BossbotHQAI.BossbotHQAI(self))

    def sendShardInfo(self):
        dg = PyDatagram()
        dg.addServerHeader(self.serverId, self.ourChannel, STATESERVER_UPDATE_SHARD)
        dg.addString(self.districtName)
        dg.addUint32(self.districtPopulation)
        self.send(dg)

    def handleConnected(self):
        self.districtId = self.allocateChannel()

        # register the AI on the state server...
        dg = PyDatagram()
        dg.addServerHeader(self.serverId, self.ourChannel, STATESERVER_ADD_SHARD)
        dg.addUint32(self.districtId)
        dg.addString(self.districtName)
        dg.addUint32(self.districtPopulation)
        self.send(dg)

        # add a post remove to remove the shard from the state server
        # when we disconnect from the message director...
        dg = PyDatagram()
        dg.addServerHeader(self.serverId, self.ourChannel, STATESERVER_REMOVE_SHARD)
        self.addPostRemove(dg)

        self.rootObj = DistributedObjectAI(self)
        self.rootObj.generateWithRequiredAndId(self.districtId, 0, 0)

        self.notify.info('Creating managers...')
        self.createManagers()

        if self.config.GetBool('want-safe-zones', True):
            self.notify.info('Creating safe zones...')
            self.createSafeZones()

        if self.config.GetBool('want-cog-headquarters', True):
            self.notify.info('Creating Cog headquarters...')
            self.createCogHeadquarters()

        self.notify.info('Done.')

    def lookupDNAFileName(self, zoneId):
        zoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        hoodId = ZoneUtil.getCanonicalHoodId(zoneId)
        hood = ToontownGlobals.dnaMap[hoodId]
        if hoodId == zoneId:
            zoneId = 'sz'
            phaseNum = ToontownGlobals.phaseMap[hoodId]
        else:
            phaseNum = ToontownGlobals.streetPhaseMap[hoodId]

        return 'phase_%s/dna/%s_%s.pdna' % (phaseNum, hood, zoneId)

    def loadDNAFileAI(self, dnastore, filename):
        return loadDNAFileAI(dnastore, filename)

    def incrementPopulation(self):
        self.districtPopulation += 1
        self.sendShardInfo()

    def decrementPopulation(self):
        self.districtPopulation -= 1
        self.sendShardInfo()

    def allocateZone(self):
        return self.zoneAllocator.allocate()

    def deallocateZone(self, zone):
        self.zoneAllocator.free(zone)

    def getZoneDataStore(self):
        return self.zoneDataStore

    def getTrackClsends(self):
        return self.wantTrackClsends

    def getAvatarExitEvent(self, avId):
        return 'distObjDelete-%d' % avId

    def trueUniqueName(self, name):
        return self.uniqueName(name)
