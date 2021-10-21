# -*- coding: UTF-8 -*-
"""
@author:Janko
@file:Client.py
@time:2021/10/20
"""
import pandas as pd
from project.GenomeInfo import GenomeInfo
from project.Genome import Genome
from project.Gene import Gene
import sys,os

class Resources(object):
 @staticmethod
 def get_url(resource_name):
     if getattr(sys, 'frozen', False):  # 是否Bundle Resource
         base_path = sys._MEIPASS
         url_path = os.path.join(base_path,"resource\\{}".format(resource_name))
         value_t = url_path.replace('\\','/')
         # print(value_t)
         return value_t
     else:
         return "{}".format(resource_name)

class Client(object):
    def __init__(self):
        self.GenomeInfoList = []
        self.get_GenomeInfoList()
        self.result_dict = {}
        self.strain = None
        self.resultList = []

    def get_GenomeInfoList(self):
        csv_path = Resources.get_url("E.coli whole genome.txt")
        df = pd.read_csv(csv_path, sep='\t')
        self.GenomeInfoList = []
        for i in range(len(df["Species"])):
            Species = df.iloc[i, 0]
            Accession = df.iloc[i, 1]
            FTP = df.iloc[i, 2]
            if (FTP == 'None'):
                continue
            else:
                FTP = "https:" + FTP[4:len(FTP)]
            obj = GenomeInfo(Species, Accession, FTP)
            self.GenomeInfoList.append(obj)
    def search(self,string):
        self.resultList = []
        for genomeInfo in self.GenomeInfoList:
            if string.lower() in genomeInfo.Species.lower():
                self.resultList.append(genomeInfo)

                # self.result_dict.update({len_t:genomeInfo})
        print(len(self.resultList))
        return self.resultList
    def dwonload_genome(self,Ecoli):
        # 将下载的内容保存
        self.strain = Genome(Ecoli)
        # print(self.strain,self.strain.genelist)

    def gene_something(self,geneObjSet):
        # 点击确定后执行以下部分
        geneSet = []
        for geneObj in geneObjSet:
            # print(geneObj.gene+' type:'+geneObj.type)
            geneObj.searchSeq(self.strain.seq)
            # geneObj.printGeneSeq()
            gene = Gene(geneObj, self.strain)
            if type(gene.geneSeq) == int:
                return gene.geneSeq
            geneSet.append(gene)

        str_list = []
        for gene in geneSet:
            str_list = gene.printGuide()

        return str_list


if __name__ == '__main__':
    pass
