class GeneSeq(object):
    def __init__(self):
        self.gene='No name'
        self.Locus_tag=''
        self.product=''
        self.note=''
        self.sequence=''
        self.type=''
        self.start=0
        self.end=0
    def searchSeq(self, seq):
        if self.type == '+':
            self.sequence = seq[self.start - 1:self.end - 1]
        else:
            for i in seq[self.start - 1:self.end - 1][::-1]:
                if i == "A":
                    self.sequence += 'T'
                if i == "T":
                    self.sequence += 'A'
                if i == "C":
                    self.sequence += 'G'
                if i == "G":
                    self.sequence += 'C'
        return self.sequence
    def printGene(self):
        print(self.gene,self.Locus_tag,self.product,self.note,sep='\t')
    def printGeneSeq(self):
        print(self.gene, self.Locus_tag, self.product, self.note, sep='\t')
        # self.sequence=self.searchSeq(self,seq)
        print(self.sequence)
        print()
    
def parseGTF(gtfPath,gname):
    genome = open(gtfPath)
    geneList = []
    while True:
        s = genome.readline()
        if not s:
            break
        ss = s.split('\t')
        if not ss[0] == gname:
            continue
        if not ss[2] == "CDS":
            continue
        sss = ss[8].split(';')
        gene = GeneSeq()
        for i in sss:
            ssss = i.split('=')
            if ssss[0] == "gene":
                gene.gene = ssss[1]
            if ssss[0] == "locus_tag":
                gene.Locus_tag = ssss[1]
            if ssss[0] == "note":
                gene.note = ssss[1]
            if ssss[0] == "product":
                gene.product = ssss[1]
        gene.type = ss[6]
        gene.start = int(ss[3])
        gene.end = int(ss[4])+1
        geneList.append(gene)
    return geneList

# file = open("Genome.txt")
# seq = file.readline().replace('\n','')
# gtfPath = "Escherichia coli strain DH5alpha chromosome, complete genome.gff"
# gname = "CP045741.1"
#
# list = parseGTF(seq,gtfPath,gname)
# for i in list:
#     print(i.gene, i.Locus_tag, i.product, i.note, i.sequence,sep='\t')