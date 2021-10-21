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
# Ecoli=search("Escherichia coli strain DH5alpha",GenomeInfoList)[0]
Ecoli=search("Nissle 1917",GenomeInfoList)
for i in Ecoli:
    print(i.Species,i.Accession)





Strain=Genome(Ecoli)


geneObj1=Strain.search('carbonic anhydrase')[0]
geneObj2=Strain.search('DapA')[0]
# geneObj3=Strain.search('GHR40_09205')[0]

# geneObjList=Strain.search('can')
# for geneObj in geneObjList:
#     geneObj.printGene()

# result=Strain.search('DapA')
# for gene in result:
#     gene.printGene()

geneObjSet=[geneObj1,geneObj2,geneObj3]

# 点击确定后执行以下部分
geneSet=[]
for geneObj in geneObjSet:
    # print(geneObj.gene+' type:'+geneObj.type)
    geneObj.searchSeq(Strain.seq)
    # geneObj.printGeneSeq()
    gene=Gene(geneObj,Strain)
    geneSet.append(gene)

for gene in geneSet:
    gene.printGuide()


