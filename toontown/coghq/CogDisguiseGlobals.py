from toontown.suit import SuitDNA
import types
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil
from otp.otpbase import OTPGlobals
from toontown.battle import SuitBattleGlobals
PartsPerSuit = (10,
 10,
 10,
 10)
PartsPerSuitBitmasks = (56411,
 56411,
 56411,
 56411)
AllBits = 56411
MinPartLoss = 1
MaxPartLoss = 2
leftLegUpper = 1
leftLegLower = 2
leftLegFoot = 4
rightLegUpper = 8
rightLegLower = 16
rightLegFoot = 32
torsoLeftShoulder = 64
torsoRightShoulder = 128
torsoChest = 256
torsoHealthMeter = 512
torsoPelvis = 1024
leftArmUpper = 2048
leftArmLower = 4096
leftArmHand = 8192
rightArmUpper = 16384
rightArmLower = 32768
rightArmHand = 65536
upperTorso = torsoLeftShoulder
leftLegIndex = 0
rightLegIndex = 1
torsoIndex = 2
leftArmIndex = 3
rightArmIndex = 4
PartsQueryShifts = (leftLegUpper,
 rightLegUpper,
 torsoLeftShoulder,
 leftArmUpper,
 rightArmUpper)
PartsQueryMasks = (leftLegFoot + leftLegLower + leftLegUpper,
 rightLegFoot + rightLegLower + rightLegUpper,
 torsoPelvis + torsoHealthMeter + torsoChest + torsoRightShoulder + torsoLeftShoulder,
 leftArmHand + leftArmLower + leftArmUpper,
 rightArmHand + rightArmLower + rightArmUpper)
PartNameStrings = TTLocalizer.CogPartNames
SimplePartNameStrings = TTLocalizer.CogPartNamesSimple
PartsQueryNames = ({1: PartNameStrings[0],
  2: PartNameStrings[1],
  4: PartNameStrings[2],
  8: PartNameStrings[3],
  16: PartNameStrings[4],
  32: PartNameStrings[5],
  64: PartNameStrings[6],
  128: PartNameStrings[7],
  256: PartNameStrings[8],
  512: PartNameStrings[9],
  1024: PartNameStrings[10],
  2048: PartNameStrings[11],
  4096: PartNameStrings[12],
  8192: PartNameStrings[13],
  16384: PartNameStrings[14],
  32768: PartNameStrings[15],
  65536: PartNameStrings[16]},
 {1: PartNameStrings[0],
  2: PartNameStrings[1],
  4: PartNameStrings[2],
  8: PartNameStrings[3],
  16: PartNameStrings[4],
  32: PartNameStrings[5],
  64: SimplePartNameStrings[0],
  128: SimplePartNameStrings[0],
  256: SimplePartNameStrings[0],
  512: SimplePartNameStrings[0],
  1024: PartNameStrings[10],
  2048: PartNameStrings[11],
  4096: PartNameStrings[12],
  8192: PartNameStrings[13],
  16384: PartNameStrings[14],
  32768: PartNameStrings[15],
  65536: PartNameStrings[16]},
 {1: PartNameStrings[0],
  2: PartNameStrings[1],
  4: PartNameStrings[2],
  8: PartNameStrings[3],
  16: PartNameStrings[4],
  32: PartNameStrings[5],
  64: SimplePartNameStrings[0],
  128: SimplePartNameStrings[0],
  256: SimplePartNameStrings[0],
  512: SimplePartNameStrings[0],
  1024: PartNameStrings[10],
  2048: PartNameStrings[11],
  4096: PartNameStrings[12],
  8192: PartNameStrings[12],
  16384: PartNameStrings[14],
  32768: PartNameStrings[15],
  65536: PartNameStrings[15]},
 {1: PartNameStrings[0],
  2: PartNameStrings[1],
  4: PartNameStrings[1],
  8: PartNameStrings[3],
  16: PartNameStrings[4],
  32: PartNameStrings[4],
  64: SimplePartNameStrings[0],
  128: SimplePartNameStrings[0],
  256: SimplePartNameStrings[0],
  512: SimplePartNameStrings[0],
  1024: PartNameStrings[10],
  2048: PartNameStrings[11],
  4096: PartNameStrings[12],
  8192: PartNameStrings[12],
  16384: PartNameStrings[14],
  32768: PartNameStrings[15],
  65536: PartNameStrings[15]})
suitTypes = PythonUtil.Enum(('NoSuit', 'NoMerits', 'FullSuit'))


def makeMeritHierarchy(baseMerits):
    meritHierarchy = []
    for _ in xrange(SuitDNA.suitsPerDept):
        meritTier = []
        for _ in xrange(SuitDNA.levelsPerSuit):
            baseMerits += (baseMerits*25) / 100
            meritTier.append(baseMerits)
        meritHierarchy.append(tuple(meritTier))
        baseMerits /= 2
    return meritHierarchy


MeritsPerLevel = makeMeritHierarchy(100)  # Bossbot
MeritsPerLevel += makeMeritHierarchy(75)  # Lawbot
MeritsPerLevel += makeMeritHierarchy(50)  # Cashbot
MeritsPerLevel += makeMeritHierarchy(25)  # Sellbot

def getNextPart(parts, partIndex, dept):
    dept = dept2deptIndex(dept)
    needMask = PartsPerSuitBitmasks[dept] & PartsQueryMasks[partIndex]
    haveMask = parts[dept] & PartsQueryMasks[partIndex]
    nextPart = ~needMask | haveMask
    nextPart = nextPart ^ nextPart + 1
    nextPart = nextPart + 1 >> 1
    return nextPart


def getPartName(partArray):
    index = 0
    for part in partArray:
        if part:
            return PartsQueryNames[index][part]
        index += 1


def isSuitComplete(parts, dept):
    dept = dept2deptIndex(dept)
    for p in xrange(len(PartsQueryMasks)):
        if getNextPart(parts, p, dept):
            return 0

    return 1


def isPaidSuitComplete(av, parts, dept):
    isPaid = 0
    base = getBase()
    if av and av.getGameAccess() == OTPGlobals.AccessFull:
        isPaid = 1
    if isPaid:
        if isSuitComplete(parts, dept):
            return 1
    return 0


def getTotalMerits(toon, index):
    from toontown.battle import SuitBattleGlobals
    cogIndex = toon.cogTypes[index] + SuitDNA.suitsPerDept * index
    cogTypeStr = SuitDNA.suitHeadTypes[cogIndex]
    cogBaseLevel = SuitBattleGlobals.SuitAttributes[cogTypeStr]['level']
    cogLevel = toon.cogLevels[index] - cogBaseLevel
    cogLevel = max(min(cogLevel, len(MeritsPerLevel[cogIndex]) - 1), 0)
    return MeritsPerLevel[cogIndex][cogLevel]


def getTotalParts(bitString, shiftWidth = 32):
    sum = 0
    for shift in xrange(0, shiftWidth):
        sum = sum + (bitString >> shift & 1)

    return sum


def asBitstring(number):
    array = []
    shift = 0
    if number == 0:
        array.insert(0, '0')
    while pow(2, shift) <= number:
        if number >> shift & 1:
            array.insert(0, '1')
        else:
            array.insert(0, '0')
        shift += 1

    str = ''
    for i in xrange(0, len(array)):
        str = str + array[i]

    return str


def asNumber(bitstring):
    num = 0
    for i in xrange(0, len(bitstring)):
        if bitstring[i] == '1':
            num += pow(2, len(bitstring) - 1 - i)

    return num


def dept2deptIndex(dept):
    if type(dept) == types.StringType:
        dept = SuitDNA.suitDepts.index(dept)
    return dept
