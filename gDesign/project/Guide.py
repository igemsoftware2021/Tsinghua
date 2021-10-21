class Guide(object):
    def __init__(self,startSite,endSite,name,sequence):
        self.name=name
        self.sequence=sequence
        self.startSite=startSite
        self.endSite=endSite

    def printGuide(self):
        # print(self.name+'\t'+self.sequence)
        return self.name+'\t'+self.sequence

