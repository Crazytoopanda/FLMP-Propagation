import scipy as sp
import math
import scipy.stats
logBase = 2


def partialEntropyAProba(proba):
    if proba == 0:
        return 0
    return -proba * math.log(proba, logBase)


def coverEntropy(cover, allNodes):  # cover is a list of set, no com ID
    allEntr = []
    for com in cover:
        fractionIn = len(com) / len(allNodes)
        allEntr.append(sp.stats.entropy([fractionIn, 1 - fractionIn], base=logBase))

    return sum(allEntr)


def comPairConditionalEntropy(cl, clKnown, allNodes):  # cl1,cl2, snapshot_communities (set of nodes)
    # H(Xi|Yj ) =H(Xi, Yj ) − H(Yj )
    # h(a,n) + h(b,n) + h(c,n) + h(d,n)
    # −h(b + d, n)−h(a + c, n)
    # a: count agreeing on not belonging
    # b: count disagreeing : not in 1 but in 2
    # c: count disagreeing : not in 2 but in 1
    # d: count agreeing on belonging
    nbNodes = len(allNodes)

    a = len((allNodes - cl) - clKnown) / nbNodes
    b = len(clKnown - cl) / nbNodes
    c = len(cl - clKnown) / nbNodes
    d = len(cl & clKnown) / nbNodes

    if partialEntropyAProba(a) + partialEntropyAProba(d) > partialEntropyAProba(b) + partialEntropyAProba(c):
        entropyKnown = sp.stats.entropy([len(clKnown) / nbNodes, 1 - len(clKnown) / nbNodes], base=logBase)
        conditionalEntropy = sp.stats.entropy([a, b, c, d], base=logBase) - entropyKnown
        # print("normal",entropyKnown,sp.stats.entropy([a,b,c,d],base=logBase))
    else:
        conditionalEntropy = sp.stats.entropy([len(cl) / nbNodes, 1 - len(cl) / nbNodes], base=logBase)
    # print("abcd",a,b,c,d,conditionalEntropy,cl,clKnown)

    return conditionalEntropy  # *nbNodes


def coverConditionalEntropy(cover, coverRef, allNodes, normalized=False):  # cover and coverRef and list of set

    allMatches = []

    for com in cover:
        matches = [(com2, comPairConditionalEntropy(com, com2, allNodes)) for com2 in coverRef]
        bestMatch = min(matches, key=lambda c: c[1])
        HXY_part = bestMatch[1]
        if normalized:
            HX = partialEntropyAProba(len(com) / len(allNodes)) + partialEntropyAProba(
                (len(allNodes) - len(com)) / len(allNodes))
            if HX == 0:
                HXY_part = 1
            else:
                HXY_part = HXY_part / HX
        allMatches.append(HXY_part)

    to_return = sum(allMatches)
    if normalized:
        to_return = to_return / len(cover)
    return to_return


def onmi(cover, coverRef, allNodes=None):  # cover and coverRef should be list of set, no community ID

    if (len(cover) == 0 and len(coverRef) != 0) or (len(cover) != 0 and len(coverRef) == 0):
        return 0
    if cover == coverRef:
        return 1

    if allNodes is None:
        allNodes = {n for c in coverRef for n in c}
        allNodes |= {n for c in cover for n in c}

    HXY = coverConditionalEntropy(cover, coverRef, allNodes)
    HYX = coverConditionalEntropy(coverRef, cover, allNodes)

    HX = coverEntropy(cover, allNodes)
    HY = coverEntropy(coverRef, allNodes)

    NMI = -10

    IXY = 0.5 * (HX - HXY + HY - HYX)
    NMI = IXY / (max(HX, HY))
    if NMI < 0 or NMI > 1 or math.isnan(NMI):
        print("NMI: %s  from %s %s %s %s " % (NMI, HXY, HYX, HX, HY))
        raise Exception("incorrect NMI")
    return NMI


def load_data(path):
    with open(path, "r") as f:
        text = f.read()
    com = []
    for line in text.split("\n"):
        arr = line.strip().split()
        arr = set(arr)
        # arr = list(map(int, arr))
        com.append(arr)
    return com

def cale_onmi(real,result):
    com1 = load_data(real)
    com2 = load_data(result)
    onmi_ = onmi(com1,com2)
    print('onmi:', onmi_)
    print('长度')
    print(len(com1))
    print(len(com2))
    for i in com2:
        print('长度com2：',len(i))
        print(i)
    for i in com1:
        print('长度com1：', len(i))
        print(i)
    return  onmi_