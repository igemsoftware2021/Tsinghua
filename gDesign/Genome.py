from Bio import Entrez
from BCBio import GFF
from Bio import SeqIO
import requests
import gzip
import os
import pprint
from BCBio.GFF import GFFExaminer
from project.seq import *

URL="https://www.ncbi.nlm.nih.gov/nuccore/"

def gz2gff(name):
    in_file = "./Cache/"+name+".gb"
    out_file = "./Cache/"+name+".gbff"
    in_handle = open(in_file)
    out_handle = open(out_file, "w")
    GFF.write(SeqIO.parse(in_handle, 'genbank'), out_handle)
    in_handle.close()
    out_handle.close()

def getGBFF(ftp, name):
    # print(len(ftp))
    index = ftp.rfind('/', 0, len(ftp) - 1)
    # print(ftp[index+1:len(ftp)])
    url = ftp + ftp[index:len(ftp)] + "_genomic.gbff.gz"
    # print(url)
    outFilePath = "./Cache/" + name + ".gbff.gz"
    myfile = requests.get(url)
    open(outFilePath, 'wb').write(myfile.content)
    f_name = outFilePath.replace(".gz", "")
    g_file = gzip.GzipFile(outFilePath)
    open(f_name, "wb+").write(g_file.read())
    g_file.close()

class Genome(object):
    def __init__(self,Ecoli):
        self.Accession=Ecoli.Accession
        self.ftp=Ecoli.FTP
        self.name=Ecoli.Species
        # url=URL+self.Accesion+"?report=fasta"
        # print(url)
        # self.sequence=Sequence(url)
        Entrez.email = "zhonglh19@mails.tsinghua.edu.cn"
        print("Loading...")
        if not os.path.exists ("./Cache") :
            os.makedirs("./Cache")

        filename = self.Accession + '.fasta'
        self.seqFilename="./Cache/"+filename
        # filename2=name+'.gb'
        if not os.path.isfile("./Cache/"+filename):
            # Downloading...
            net_handle = Entrez.efetch(db="nucleotide", id=self.Accession, rettype="fasta", retmode="text")
            # gb_handle2= Entrez.efetch(db="nucleotide", id=self.Accesion, rettype="gb", retmode="text")
            out_handle = open("./Cache/"+filename, "w")
            # out_gb_handle=open("./Cache/"+filename2,'w')
            out_handle.write(net_handle.read())
            # out_gb_handle.write(gb_handle2.read())
            out_handle.close()
            # out_gb_handle.close()
            net_handle.close()
            # gb_handle2.close()
            # gz2gff(name)
            print("Fasta Saved")
        if not os.path.isfile("./Cache/"+self.Accession+'.gbff'):
            getGBFF(self.ftp, self.Accession)
            print ("Gbff Saved")
        if not os.path.isfile("./Cache/"+self.Accession+'.gff'):
            self.parseGBFF(self.Accession)
            print ("Gff Saved")

        print ("Parsing...")
        record = SeqIO.read("./Cache/"+filename, "fasta")
        self.seq=record.seq
        # File = open("Genome.txt", "w")
        # File.write(str(self.seq))
        # File.close()
        self.genelist = self.parseGFF(str(self.seq), "./Cache/" + self.Accession + '.gff', self.Accession)
        # data=''
        # for i in self.genelist:
        #     data=data+i.gene+'\t'+ i.Locus_tag+'\t'+i.product+'\t'+i.note+'\t'+i.sequence+'\n'
        # File = open("Genome.txt", "w")
        # File.write(data)
        # File.close()
        # result=search('carbonic ',self.genelist)
        # for gene in result:
        #     gene.printGeneSeq()

    def search(self,name):
        gresult = []
        presult = []
        nresult = []
        lresult = []
        for i in self.genelist:
            if name.lower() in i.gene.lower():
                gresult.append(i)
            elif name.lower() in i.product.lower():
                presult.append(i)
            elif name.lower() in i.note.lower():
                nresult.append(i)
            elif name.lower() in i.Locus_tag.lower():
                lresult.append(i)
        return gresult + presult + nresult + lresult

    def parseGFF(self,seq, gtfPath, gname):             #parseGFF
        if "NZ_" in gname:
            gname = gname.replace("NZ_", '')
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
            if ss[3] == '1':
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


    def parseGBFF(self,name):           #parseGBFF to GFF
        # print(path)
        # in_file="./Cache/GCA_009648495.1_ASM964849v1_genomic.gff"
        in_file = "./Cache/" + name + '.gbff'
        out_file = "./Cache/" + name + '.gff'       #Gff file
        in_handle = open(in_file)
        out_handle = open(out_file, "w")
        GFF.write(SeqIO.parse(in_handle, "genbank"), out_handle)
        in_handle.close()
        out_handle.close()



