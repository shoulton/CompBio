import sys

lines = []
l = sys.stdin.readline()
while l != "\n":
    lines.append(l)
    l = sys.stdin.readline()

seqdict = {}
descriptor = ''
seq = ''

for line in lines:

    if line[0] == '>':
        if descriptor:
            seqdict[descriptor] = seq
            seq = ''
        descriptor = line[1:]
    else:
        seq = seq + line
seqdict[descriptor] = seq
print(seqdict)
