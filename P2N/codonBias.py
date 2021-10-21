from AminoAcid import *
from Codon import *

class codonBias(object):
    def __init__(self, context):
        self.context = context
        self.parseCodonTable()

    def parseCodonTable(self):
        cursorIndex1 = 1
        cursorIndex2 = 0
        self.myCodonTable = []
        for k in range(0, 4):
            for i in range(0, 4):
                for j in range(0, 4):
                    codonTriplet = self.context[cursorIndex1:cursorIndex1 + 3]
                    cursorIndex1 = cursorIndex1 + 4
                    cursorIndex2 = self.context.find("(", cursorIndex1)
                    codonFriquency = float(str(self.context[cursorIndex1:cursorIndex2]))
                    cursorIndex2 = self.context.find(")", cursorIndex2)
                    cursorIndex1 = cursorIndex2 + 3
                    self.myCodonTable.append(codon(codonTriplet, codonFriquency))
                cursorIndex1 = cursorIndex1 - 1
            cursorIndex1 = cursorIndex1 + 1

        # for i in self.myCodonTable:
        #     i.printCodonInfo()
        self.createAminoAcidSet()

    def getCodonObject(self, codonTriplet):
        for codon in self.myCodonTable:
            if (codon.triplet == codonTriplet):
                return codon
        pass

    def createAminoAcidSet(self):
        self.myAminoAcidSet = []
        Phe = AminoAcid('F', [self.getCodonObject("UUU")
            , self.getCodonObject("UUC")])
        self.myAminoAcidSet.append(Phe)

        Leu = AminoAcid('L', [self.getCodonObject("UUA")
            , self.getCodonObject("UUG")
            , self.getCodonObject("CUC")
            , self.getCodonObject("CUG")
            , self.getCodonObject("CUA")
            , self.getCodonObject("CUU")])
        self.myAminoAcidSet.append(Leu)

        Ser = AminoAcid('S', [self.getCodonObject("UCU")
            , self.getCodonObject("UCC")
            , self.getCodonObject("UCA")
            , self.getCodonObject("UCG")
            , self.getCodonObject("AGU")
            , self.getCodonObject("AGC")])
        self.myAminoAcidSet.append(Ser)

        Tyr = AminoAcid('Y', [self.getCodonObject("UAU")
            , self.getCodonObject("UAC")])
        self.myAminoAcidSet.append(Tyr)

        Cys = AminoAcid('C', [self.getCodonObject("UGU")
            , self.getCodonObject("UGC")])
        self.myAminoAcidSet.append(Cys)

        Pro = AminoAcid('P', [self.getCodonObject("CCU")
            , self.getCodonObject("CCC")
            , self.getCodonObject("CCA")
            , self.getCodonObject("CCG")])
        self.myAminoAcidSet.append(Pro)

        His = AminoAcid('H', [self.getCodonObject("CAU")
            , self.getCodonObject("CAC")])
        self.myAminoAcidSet.append(His)

        Gln = AminoAcid('Q', [self.getCodonObject("CAA")
            , self.getCodonObject("CAG")])
        self.myAminoAcidSet.append(Gln)

        Trp = AminoAcid('W', [self.getCodonObject("UGG")])
        self.myAminoAcidSet.append(Trp)

        Arg = AminoAcid('R', [self.getCodonObject("AGA")
            , self.getCodonObject("AGG")
            , self.getCodonObject("CGU")
            , self.getCodonObject("CGC")
            , self.getCodonObject("CGA")
            , self.getCodonObject("CGG")])
        self.myAminoAcidSet.append(Arg)

        Ile = AminoAcid('I', [self.getCodonObject("AUU")
            , self.getCodonObject("AUC")
            , self.getCodonObject("AUA")])
        self.myAminoAcidSet.append(Ile)

        Met = AminoAcid('M', [self.getCodonObject("AUG")])
        self.myAminoAcidSet.append(Met)

        Thr = AminoAcid('T', [self.getCodonObject("ACU")
            , self.getCodonObject("ACC")
            , self.getCodonObject("ACA")
            , self.getCodonObject("ACG")])
        self.myAminoAcidSet.append(Thr)

        Asn = AminoAcid('N', [self.getCodonObject("AAU")
            , self.getCodonObject("AAC")])
        self.myAminoAcidSet.append(Asn)

        Lys = AminoAcid('K', [self.getCodonObject("AAA")
            , self.getCodonObject("AAG")])
        self.myAminoAcidSet.append(Lys)

        Val = AminoAcid('V', [self.getCodonObject("GUU")
            , self.getCodonObject("GUC")
            , self.getCodonObject("GUA")
            , self.getCodonObject("GUG")])
        self.myAminoAcidSet.append(Val)

        Ala = AminoAcid('A', [self.getCodonObject("GCU")
            , self.getCodonObject("GCC")
            , self.getCodonObject("GCA")
            , self.getCodonObject("GCG")])
        self.myAminoAcidSet.append(Ala)

        Asp = AminoAcid('D', [self.getCodonObject("GAU")
            , self.getCodonObject("GAC")])
        self.myAminoAcidSet.append(Asp)

        Glu = AminoAcid('E', [self.getCodonObject("GAA")
            , self.getCodonObject("GAG")])
        self.myAminoAcidSet.append(Glu)

        Gly = AminoAcid('G', [self.getCodonObject("GGU")
            , self.getCodonObject("GGC")
            , self.getCodonObject("GGA")
            , self.getCodonObject("GGG")])
        self.myAminoAcidSet.append(Gly)

        Stop = AminoAcid('*', [self.getCodonObject("UAA")
            , self.getCodonObject("UAG")
            , self.getCodonObject("UGA")])
        self.myAminoAcidSet.append(Stop)

        for aminoAcid in self.myAminoAcidSet:
            aminoAcid.getTheMostPreferencedCodon()

        # for aminoAcid in self.myAminoAcidSet:
        #     aminoAcid.printInfo()
