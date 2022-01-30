import sys

def readCodon(codonFile):
    with open(codonFile) as cf:
        line = cf.readline()
        codonDict = {}
        while line:
            splitLine = line.split()
            nucleotides = splitLine[0].strip()
            acid = splitLine[1].strip()
            codonDict[nucleotides] = acid
            line = cf.readline()
    return codonDict

def readFasta():
    l = sys.stdin.read()
    lines = l.split("\n")

    seqdict = {}
    descriptor = ''
    seq = ''

    for line in lines:
        if line:
            if line[0] == '>':
                if descriptor:
                    seqdict[descriptor] = seq
                    seq = ''
                descriptor = line[1:]
            else:
                seq = seq + line
    seqdict[descriptor] = seq
    return seqdict

def translate(codonDict, fastaDict):
    keys = list(fastaDict.keys())
    translatedSeq = ''
    for key in keys:
        seq = fastaDict[key].strip()
        trio = ''
        for char in seq:
            if len(trio) < 3:
                trio = trio + char
            if len(trio) == 3:
                translatedSeq = translatedSeq + codonDict.get(trio)
                trio = ''
        print(">" + key + "\n" + translatedSeq + "\n")

if __name__ == "__main__":
    codonFile = 'codon_table.txt'
    codonDict = readCodon(codonFile)
    fastaDict = readFasta()
    translate(codonDict, fastaDict)
