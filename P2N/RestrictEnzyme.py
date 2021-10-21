class RestrictEnzyme(object):
    def __init__(self,name,recognitionSite):
        self.name=name
        self.recognitionSite=recognitionSite
    def printRE(self):
        print('Name:'+self.name+'\tRecognition Site:'+self.recognitionSite)
    def getREMessage(self):
        return self.name+'\t'+self.recognitionSite+'\n'