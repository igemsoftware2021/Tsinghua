class GenomeInfo(object):
    def __init__(self,Species,Accession,FTP):
        self.Species=Species
        self.Accession=Accession
        self.FTP=FTP
    def printGenomeInfo(self):
        print(self.Species,self.Accession,self.FTP,sep='\t')