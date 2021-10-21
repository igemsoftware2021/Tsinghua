class CodonTable(object):
    def __init__(self):
        self.myDict = {
            'UUU': 'F', 'UUC': 'F',
            'UUA': 'L', 'UUG': 'L', 'CUU': 'L', 'CUG': 'L', 'CUC': 'L', 'CUA': 'L',
            'AGU': 'S', 'AGC': 'S', 'UCU': 'S', 'UCG': 'S', 'UCC': 'S', 'UCA': 'S',
            'UGU': 'C', 'UGC': 'C',
            'UAU': 'Y', 'UAC': 'Y',
            'CCU': 'P', 'CCG': 'P', 'CCC': 'P', 'CCA': 'P',
            'CAU': 'H', 'CAC': 'H',
            'CAA': 'Q', 'CAG': 'Q',
            'UGG': 'W',
            'AGA': 'R', 'AGG': 'R', 'CGU': 'R', 'CGG': 'R', 'CGC': 'R', 'CGA': 'R',
            'AUU': 'I', 'AUC': 'I', 'AUA': 'I',
            'AUG': 'M',
            'ACU': 'T', 'ACG': 'T', 'ACC': 'T', 'ACA': 'T',
            'AAC': 'N', 'AAU': 'N',
            'AAA': 'K', 'AAG': 'K',
            'GUU': 'V', 'GUG': 'V', 'GUC': 'V', 'GUA': 'V',
            'GCU': 'A', 'GCG': 'A', 'GCC': 'A', 'GCA': 'A',
            'GAU': 'D', 'GAC': 'D',
            'GAA': 'E', 'GAG': 'E',
            'GGU': 'G', 'GGG': 'G', 'GGC': 'G', 'GGA': 'G',
            'UAA': '*', 'UAG': '*', 'UGA': '*'
        }

    def getAminoAcid(self,triplet):
        return self.myDict[triplet]