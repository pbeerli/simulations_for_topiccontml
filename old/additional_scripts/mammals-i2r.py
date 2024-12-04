#!/usr/bin/env python3
#
# change interleaved format to non-interleaved
#
import sys
import os


def read_file(file):
    with open(file,'r') as f:
        headline = f.readline()
        head = headline.split()
        numind = int(head[0])
        sites = int(head[1])
        data = []
        for i in range(numind):
            a = f.readline().rstrip()
            ind,seq = a.split()
            na = f'{ind:10}{seq}'
            data.append(na)
        i=0
        for line in f:
            if line.strip()=='':
                continue
            else:
                if i==numind:
                    i=0                    
                data[i] += line.strip()
                i +=1
        for i in range(len(data)):
            data[i] += '\n'
    return headline,data


if __name__ == "__main__":
    arr = os.listdir()
    for fi,file in enumerate(arr):
        header, data = read_file(file)
        fw = open('../loci/locus'+str(fi)+".txt",'w')
        fw.write(header)
        for di in data:
            fw.write(di)

