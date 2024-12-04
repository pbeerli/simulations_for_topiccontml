#!/usr/bin/env python
# coding: utf-8

data=[]
with open('infile10','r') as f:
    for fi in f:
        data.append(fi.rstrip())

numpop, numloci,*ll = data[0].split()

sites = [int(i) for i in data[1].split()]

ind = [int(i) for i in data[2].split()[:14]]
popname = data[2].split()[14]

start = 2
loci = []
for z in range(int(numpop)):
    ind = [int(i) for i in data[start].split()[:14]]
    popname = data[start].split()[14]
    start += 1
    for index,i in enumerate(ind):
        loci.append([])
        for j in range(i):
            loci[index].append(f'{popname[:3]}'+data[start+j])
        start = start + j + 1
#
for i in range(int(numloci)):
    with open(f"locus{i}.txt",'w') as f:
        numind = len(loci[i])
        f.write(f'{numind} {sites[i]} Locus{i}\n')
        for j in range(numind):
            f.write(loci[i][j])
            f.write('\n')
