class codon(object):
    def __init__(self,triplet,frequency):
        self.triplet=triplet
        self.frequency=frequency
    def printCodonInfo(self):       #for debug
        print("Triplet: "+self.triplet+"\tFrequency: "+str(self.frequency))
