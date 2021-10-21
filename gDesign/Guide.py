class Guide(object):
    def __init__(self,startSite,endSite,name,sequence):
        self.name=name
        self.sequence=sequence
        self.startSite=startSite
        self.endSite=endSite

    def setName(self,number):
        self.name=self.name+'-'+str(number)

    def printGuide(self):
        # file = open("E:/iGEM/final/Software/Biosafety+CRISPR_AID/gDesign/V1+/project/result.txt",'a')
        # file.write(self.name+'\t'+str(self.sequence)+'\n')
        print(self.name,self.sequence,sep='\t')


