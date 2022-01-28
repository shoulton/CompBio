import sys

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
print(seqdict)
