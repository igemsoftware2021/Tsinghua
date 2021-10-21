from project.Gene import Gene
from project.Genome import Genome
# First, input gene sequence as original data
# And extract basic information from it
import pandas as pd
from project.GenomeInfo import GenomeInfo

df = pd.read_csv("../E.coli whole genome.txt", sep ='\t')
GenomeInfoList=[]
for i in range(len(df["Species"])):
    Species = df.iloc[i,0]
    Accession = df.iloc[i,1]
    FTP=df.iloc[i,2]
    if(FTP=='None'):
        continue
    else:
        FTP="https:"+FTP[4:len(FTP)]
    obj=GenomeInfo(Species,Accession,FTP)
    GenomeInfoList.append(obj)

def search(string,GenomeInfoList):
    resultList=[]
    for genomeInfo in GenomeInfoList:
        # print(genomeInfo.Species)
        if string.lower() in genomeInfo.Species.lower():
            resultList.append(genomeInfo)
    return resultList

# name="Escherichia coli strain DH5alpha chromosome, complete genome"
Ecoli=search("Nissle 1917",GenomeInfoList)[0]
# print(Ecoli)

# for strain in Ecoli:
#     print(strain.Species)

type='NGG'
choose='Genome screen'

Strain=Genome(Ecoli)

# list=Strain.search('carbonic anhydrase')
# for i in list:
#     i.printGene()

geneObj1=Strain.search('carbonic anhydrase')[0]
geneObj2=Strain.search('DapA')[0]
# geneObj3=Strain.search('GHR40_09205')[0]

# geneObj1.printGene()

# geneObjList=Strain.search('can')
# for geneObj in geneObjList:
#     geneObj.printGene()

# result=Strain.search('DapA')
# for gene in result:
#     gene.printGene()

geneObjSet=[geneObj1,geneObj2]

geneObjSet=Strain.genelist


geneSet=[]

geneObjSet[0].printGene()
print("Calculation...")
for geneObj in geneObjSet:
    print(geneObj.Locus_tag)
    geneObj.searchSeq(Strain.seq)
    #geneObj.printGene()
    # geneObj.printGeneSeq()
    # print('Calculation '+geneObj.product+' ...')
    gene=Gene(geneObj,Strain,type,choose)
    geneSet.append(gene)
print("Done!")

for gene in geneSet:
    gene.printGuide()
