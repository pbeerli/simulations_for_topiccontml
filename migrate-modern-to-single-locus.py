#!/usr/bin/env python
# coding: utf-8
import sys
import os

if len(sys.argv) < 2:
    print('syntax: python migrate-modern-t0-single-locus.py infile')
    print('creates a folder with simdata-infilename')
    sys.exit()
else:
    infile = sys.argv[1]

def create_single_loci(start,numloci, numpop, data, sites):
    loci =[ [] for i in range(int(numloci))]
    popnames=[]
    for z in range(int(numpop)):
        oneind = [int(i) for i in data[start].split()[:1]][0]
        popname = data[start].split()[1]
        popnames.append(popname)
        start += 1
        for ind in range(oneind):
            sitestart = 0
            for locus, site in enumerate(sites):
                name,newdata = data[start+ind].split()
                loci[locus].append(
                    f'{popname[:4]}{ind}   '+newdata[sitestart:sitestart+site])
                sitestart += site
        print(start,data[start][:20],data[start][-20:])
        start = start + oneind 
    return loci,popnames

def write_single(numloci,loci,sites,popnames,folder):
    os.system(f'mkdir {folder}')
    with open(f"{folder}/popnames.txt",'w') as pf:
        for pop in popnames:
            pf.write(pop+'\n')
            
    for i in range(int(numloci)):
        with open(f"{folder}/locus{i}.txt",'w') as f:
            numind = len(loci[i])
            f.write(f'{numind} {sites[i]} Locus{i}\n')
            for j in range(numind):
                name,sequence = loci[i][j].split()
                f.write(f"{name:10}{sequence}")
                f.write('\n')
    

if __name__ == '__main__':
    data=[]
    with open(infile,'r') as f:
        for fi in f:
            if fi[0] == '#':
                continue
            data.append(fi.rstrip())
    numpop, numloci,*ll = data[0].split()
    sites = [int(i.replace('(','').replace(')','').replace('s','')) for i in data[1].split()]
    start=2
    loci,popnames = create_single_loci(start,numloci, numpop, data, sites)
    folder = 'sim'+infile
    write_single(numloci,loci,sites,popnames,folder)
    
