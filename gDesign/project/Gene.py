import sys

from project.Guide import *
from project.func.func_basicFunction import *
from project.func.func_generateGRNASeq import *
from project.Genome import *

def align_SW(sgSeq, genomeSeq):
    scoringMat = {"AA": 5, "AT": -4, "AC": -4, "AG": -4,
                  "TA": -4, "TT": 5, "TC": -4, "TG": -4,
                  "CA": -4, "CT": -4, "CC": 5, "CG": -4,
                  "GA": -4, "GT": -4, "GC": -4, "GG": 5}
    sgLen = len(sgSeq)
    genomeLen = len(genomeSeq)
    scoring = [[0] * (genomeLen + 1) for i in range(sgLen + 1)]
    comeFrom = [[3] * (genomeLen + 1) for i in range(sgLen + 1)]
    hitSite = [0] * genomeLen
    hit = 0
    for i in range(1, sgLen + 1):
        for j in range(1, genomeLen + 1):
            r1 = scoring[i - 1][j - 1] + scoringMat[sgSeq[i - 1] + genomeSeq[j - 1]]
            r2 = scoring[i - 1][j] - 4
            r3 = scoring[i][j - 1] - 4
            r4 = 0
            r = [r1, r2, r3, r4]
            scoring[i][j] = max(r)
            comeFrom[i][j] = r.index(max(r))
    for i in range(sgLen - 2, sgLen):
        for j in range(genomeLen):
            if scoring[i][j] >= (len(sgSeq) - 2) * 5:
                ii = i
                jj = j
                while comeFrom[ii][jj] != 3:
                    if hitSite[jj - 1] == 0:
                        hitSite[jj - 1] = 1
                        hit += 1
                    if comeFrom[ii][jj] == 0:
                        ii -= 1
                        jj -= 1
                    elif comeFrom[ii][jj] == 1:
                        ii -= 1
                    else:
                        jj -= 1
    return 10 - hit / (sgLen + 0.0)

class Gene(object):
    def __init__(self,geneObj,strain,type,choose):
        self.choose=choose
        self.geneObj=geneObj
        self.getGeneName()
        self.strain=strain
        self.geneSeq=self.getGeneSeq()
        self.GuideList=[]
        self.guideNumber=0
        self.calculationGRNASeq(self.geneSeq,type)
        self.calculationGRNASeq(toAntisense(self.geneSeq),type, direction="antisense")
        # self.guideRank()

    # def guideScore(self):
    #     for guide in self.GuideList:
    #         myScore=align_SW(guide.sequence,self.strain.seq)

    def guideRank(self):
        self.GuideList.sort(key=lambda x:x.score)
        i=0
        for guide in self.GuideList:
            i=i+1
            guide.setName(i)

    def getGeneName(self):
        if not self.geneObj.gene=='No name':
            self.geneName=self.geneObj.gene
        else:
            self.geneName=self.geneObj.product


    def getGeneSeq(self):
        self.geneSeq = self.geneObj.sequence
        #geneSeq=getGene(self.geneName)
        geneSeq = self.geneSeq.upper()
        geneLen = len(geneSeq)
        # Check if the input meets standard DNA sequence
        if (self.choose=='Single gene'):
            for c in geneSeq:
                if c not in "ATCG":
                    print("Unknown base detected, please check whether any other character except for ATCG exists.")
                    sys.exit()
            if geneLen % 3 != 0:
                print("Incorrect sequence length detected, please check the input.")
            if ((geneSeq[:3] !=("ATG")) & (geneSeq[:3] !=("TTG")) & (geneSeq[:3] !=("GTG")) & (geneSeq[:3] !=("CTG"))):
                print("No start codon ATG or TTG or GTG or CTG detected, please check the input.")
                sys.exit()
            if geneSeq[-3:] != "TAA" and geneSeq[-3:] != "TGA" and geneSeq[-3:] != "TAG":
                print("No stop codon detected, please check the input.")
                sys.exit()
            codonNum = geneLen // 3
            for i in range(codonNum - 1):
                codon = geneSeq[i * 3:i * 3 + 3]
                if codon == "TAA" or codon == "TAG" or codon == "TGA":
                    print("A pre-exist stop codon detected, please check the input.")
                    sys.exit()
            # print("Eligible input. Available gRNA sequences are listed below:")
        elif (self.choose=='Genome screen'):
            pass
        return geneSeq

    def calculationGRNASeq(self,geneSeq,type,direction="sense"):
        if type == "NGG":
            checkPos = 3
            checkCont = ("GG",)
        elif type == "NG":
            checkPos = 2
            checkCont = ("G",)
        elif type == "NRN":
            checkPos = 3
            checkCont = ("AA", "AT", "AG", "AC", "GA", "GT", "GG", "GC")
        else:
            ex = Exception("Wrong base editor type assigned for printGRNASeq()")
            raise ex
        # Upper case input required!
        geneLen = len(geneSeq)
        codonNum = geneLen // 3
        for i in range(codonNum):
            codon = geneSeq[i * 3:i * 3 + 3]
            if direction == "sense":
                if codon == "CAA" or codon == "CAG" or codon == "CGA":
                    for j in range(i * 3 + 18, i * 3 + 22):
                        if j + 2 >= geneLen: break
                        if geneSeq[j + 1:j + checkPos] in checkCont:
                            # NGG found
                            if i - 2 < 0: continue
                            # Alternative: Search from the 2nd codon instead of the 1st
                            fr = i * 3 - 2
                            to = j
                            self.guideNumber+=1
                            thisName=self.geneName+'-'+str(self.guideNumber)
                            # thisName=self.geneName
                            # print("Blast "+thisName)
                            # thisScore=align_SW(geneSeq[fr:to],self.strain.seq)-self.guideNumber*0.5
                            thisguide=Guide(fr,to,thisName,geneSeq[fr:to])
                            self.GuideList.append(thisguide)


            elif direction == "antisense":
                if codon == "CCA":
                    for j in range(i * 3 + 18, i * 3 + 23):
                        if j + 2 >= geneLen: break
                        if geneSeq[j + 1:j + checkPos] in checkCont:
                            if i - 2 < 0: continue
                            fr = i * 3 - 2
                            to = j
                            self.guideNumber = self.guideNumber + 1
                            thisName = self.geneName + '-' + str(self.guideNumber)
                            # thisName = self.geneName
                            # thisScore = align_SW(geneSeq[fr:to], self.strain.seq) - str(self.guideNumber) * 0.5
                            thisguide = Guide(fr, to, thisName, geneSeq[fr:to])
                            self.GuideList.append(thisguide)

    def printGuide(self):
        for guide in self.GuideList:
            guide.printGuide()