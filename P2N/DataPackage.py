from random import *
from CodonTable import *
from RESiteDict import *
from Downloader import *

class DataPackage(object):
    def __init__(self,species,choice):
        self.species = species
        #self.aaSequence = aaSequence.upper()
        self.choice = choice
        self.url = self.getWebSite()
        self.myREDict=RESiteDict()

    def getWebSite(self):
        mySearch = Search(self.species)
        return mySearch.link_getter()

    def setaaSequence(self,aaSequence):
        self.aaSequence=aaSequence.upper()

    def setDNASequence(self, DNASequence):
        self.DNASequence=DNASequence.upper()
        self.Translation()

    def setAvoidREList(self,REList):
        self.avoidREList=REList

    def Translation(self):
        self.CalculationD2R()
        self.CalculationR2P()

    def CalculationR2P(self):
        self.aaSequence=''
        codonNumber=int(len(self.mRNASequence)/3)
        for i in range(0,codonNumber):
            triplet=self.mRNASequence[i*3:(i+1)*3]
            # print(triplet)
            AminoAcid=self.getAminoAcid(triplet)
            self.aaSequence=self.aaSequence+AminoAcid
        #print(self.aaSequence)

    def getAminoAcid(self,triplet):
        myCodonTable=CodonTable()
        return myCodonTable.getAminoAcid(triplet)

    def getAminoAcidObject(self,triplet):
        myCodonTable = CodonTable()
        AminoAcidName=myCodonTable.getAminoAcid(triplet)
        for AminoAcid in self.myCodonBias.myAminoAcidSet:
            if(AminoAcidName==AminoAcid.name):
                return AminoAcid

    def setCodonBias(self,CodonBias):
        self.myCodonBias = CodonBias

    def isAminoAcid(self,AminoAcidName):
        for aminoAcid in self.myCodonBias.myAminoAcidSet:
            if(AminoAcidName==aminoAcid.name):
                return True
        return False

    def getCodonObject(self, AminoAcidName):
        myAminoAcid=None
        for AminoAcid in self.myCodonBias.myAminoAcidSet:
            if(AminoAcidName==AminoAcid.name):
                myAminoAcid=AminoAcid
                break
        if (AminoAcidName=='*'):
            total_value=0
            for codon in myAminoAcid.codonSet:
                total_value=total_value+codon.frequency
            random_value=random.random()*total_value
            a=0
            for codon in myAminoAcid.codonSet:
                b = a+codon.frequency
                if((random_value>a)&(random_value<=b)):
                    return codon
                else:
                    a=b
        else:
            return self.getTriplet(myAminoAcid)

    def getTriplet(self, myAminoAcid):
        total_value = 0
        for codon in myAminoAcid.permissionCodonSet:
            total_value = total_value + codon.frequency
        random_value = random.random() * total_value
        a = 0
        for codon in myAminoAcid.codonSet:
            b = a + codon.frequency
            if ((random_value > a) & (random_value <= b)):
                return codon
            else:
                a = b

    def getAvoidTriplet(self, myAminoAcid, avoidTriplet):
        total_value = 0
        for codon in myAminoAcid.permissionCodonSet:
            if (codon.triplet==avoidTriplet):
                total_value=total_value
            else:
                total_value = total_value + codon.frequency
        random_value = random.random() * total_value
        a = 0
        for codon in myAminoAcid.codonSet:
            if(codon.triplet==avoidTriplet):
                continue
            else:
                b = a + codon.frequency
                if ((random_value > a) & (random_value <= b)):
                    return codon
                else:
                    a = b

    def isExistRESite(self,RESite):
        if(self.DNASequence.find(RESite)!=-1):
            return True
        else:
            return False

    def CalculationP2N(self):
        if(self.aaSequence[-1]!='*'):
            self.aaSequence=self.aaSequence+"*"
        #print(self.aaSequence)
        self.mRNASequence=''
        for aa in self.aaSequence:
            if (self.isAminoAcid(aa)):
                codon=self.getCodonObject(aa)
                self.mRNASequence=self.mRNASequence+codon.triplet
            else:
                print('Error!!!')
                break
        self.CalculationR2D()
        #print(self.DNASequence)
        if (len(self.avoidREList)>0):
            self.avoidRESiteList=self.myREDict.getRestrictionSiteList(self.avoidREList)
            for RESite in self.avoidRESiteList:
                #print(RESite+': '+str(self.isExistRESite(RESite)))
                if(self.isExistRESite(RESite)==True):
                    position=self.DNASequence.find(RESite)
                    index1=(int(position/3))*3
                    index2=index1+3
                    avoidTriplet=self.DNASequence[index1:index2]
                    print(avoidTriplet)
                    AminoAcid = self.getAminoAcidObject(avoidTriplet)
                    modifiedTriplet=self.getAvoidTriplet(AminoAcid,avoidTriplet)
                    self.DNASequence=self.DNASequence[:index1]+modifiedTriplet.triplet+self.DNASequence[index2:]
            self.CalculationD2R()

        #print(self.mRNASequence)
        #print(self.DNASequence)

    def CalculationR2D(self):
        self.DNASequence=''
        for base in self.mRNASequence:
            if(base=='U'):
                self.DNASequence=self.DNASequence+'T'
            else:
                self.DNASequence = self.DNASequence + base

    def CalculationD2R(self):
        self.mRNASequence=''
        # print(self.DNASequence)
        for base in self.DNASequence:
            if(base=='T'):
                self.mRNASequence=self.mRNASequence+'U'
            else:
                self.mRNASequence = self.mRNASequence + base
        # print(self.mRNASequence)


