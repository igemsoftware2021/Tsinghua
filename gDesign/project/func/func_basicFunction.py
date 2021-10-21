def toComplementBase(base):
    if base == "A": return "T"
    if base == "T": return "A"
    if base == "G": return "C"
    if base == "C": return "G"

def toAntisense(senseSeq):
    seqLen = len(senseSeq)
    res = ""
    for i in range(seqLen):
        res = toComplementBase(senseSeq[i]) + res
    return res