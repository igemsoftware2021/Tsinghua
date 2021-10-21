import math

class AminoAcid(object):
    def __init__(self,name,codonSet):
        self.name=name
        self.codonSet=codonSet
    def getCodonSet(self):
        return self.codonSet
    def getTheMostPreferencedCodon(self):
        for i in range(0,len(self.codonSet)-1):
            for j in range(0,len(self.codonSet)-i-1):
                if(self.codonSet[j].frequency<self.codonSet[j+1].frequency):
                    tem=self.codonSet[j]
                    self.codonSet[j]=self.codonSet[j+1]
                    self.codonSet[j+1]=tem
        sumCodonFrequency=0
        for codon in self.codonSet:
            sumCodonFrequency=sumCodonFrequency+codon.frequency
        average=sumCodonFrequency/len(self.codonSet)
        # print(average)
        sumErrorMeanSquare=0
        for codon in self.codonSet:
            sumErrorMeanSquare=sumErrorMeanSquare\
                               +(codon.frequency-average)*(codon.frequency-average)
        if(len(self.codonSet)!=1):
            Varience=math.sqrt(sumErrorMeanSquare/(len(self.codonSet)-1))
        else:
            Varience=math.sqrt(sumErrorMeanSquare/len(self.codonSet))
        if(Varience!=0):
            if((average/Varience)<2):
                self.threshold=average-Varience/3
            elif(((average/Varience)>=2)&((average/Varience)<4)):
                self.threshold = average - Varience/2
            else:
                self.threshold=average-Varience
        else:
            self.threshold=average

        self.getpermissionCodonSet()

    def printInfo(self):
        print(self.name+":")
        for codon in self.codonSet:
            codon.printCodonInfo()
        print('Threshold='+str(self.threshold))
        print('\nPermissioned:')
        for codon in self.permissionCodonSet:
            codon.printCodonInfo()
        print()

    def getpermissionCodonSet(self):
        self.permissionCodonSet=[]
        for codon in self.codonSet:
            if(codon.frequency>=self.threshold):
                self.permissionCodonSet.append(codon)

