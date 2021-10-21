def printGRNASeq(geneSeq, direction="sense"):
    # Upper case input required!
    geneLen = len(geneSeq)
    codonNum = geneLen // 3
    for i in range(codonNum):
        codon = geneSeq[i * 3:i * 3 + 3]
        if direction == "sense":
            if codon == "CAA" or codon == "CAG" or codon == "CGA":
                for j in range(i * 3 + 18, i * 3 + 22):
                    if j + 2 >= geneLen: break
                    if geneSeq[j + 1:j + 3] == "GG":
                        # NGG found
                        if i - 2 < 0: continue
                        # Alternative: Search from the 2nd codon instead of the 1st
                        fr = i * 3 - 2
                        to = j
                        print("(%d)"%(fr + 1), end="\t")
                        print(geneSeq[fr:to], end="\t")
                        print("(%d)"%(to),end="\t")
                        print("%d"%(fr + 3))
        elif direction == "antisense":
            if codon == "CCA":
                for j in range(i * 3 + 18, i * 3 + 23):
                    if j + 2 >= geneLen: break
                    if geneSeq[j + 1:j + 3] == "GG":
                        if i - 2 < 0: continue
                        fr = i * 3 - 2
                        to = j
                        print("(%d)"%(geneLen - fr), end="\t")
                        print(geneSeq[fr:to], end="\t")
                        print("(%d)"%(geneLen - to + 1), end="\t")
                        print("%d/%d"%(geneLen - fr - 3, geneLen - fr - 2))