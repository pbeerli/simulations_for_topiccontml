#!/usr/bin/env python
# running simulation with dawg
# design 1,2,5,10 loci each 10 reps
# with specific random number seeds so that we do not need to store all parts
#
import random
import os
import sys

def read_template(myfile):
    with open(myfile, 'r') as f:
        return "".join(f.readlines())

def read_tree(treefile):
    return read_template(treefile)

def count_tips(treestring):
    elements = treestring.replace(" ", "").split(",")
    tip_count = sum(1 for elem in elements if not elem.endswith(")"))
    return tip_count

def write_dawg(fs, st):
    with open(fs,'w') as f:
        f.write(st)

# creates the locusX.txt files
def run_dawg(treestring, seed, reps):
    template = read_template('dna-with-gaps.dawg')
    print(template)
    print(treestring)
    template = template.replace('theTree',treestring)
    tips = count_tips(treestring)
    allnodes = tips + (tips - 2) # unrooted
    write_dawg('temp.dawg', template)
    os.system(f"dawg temp.dawg --split --seed {seed} --reps {reps}")
    os.system("ls simdata* | awk '{print \"grep -v ^Z \"$0,\"> locus\"NR-1\".txt\"}' | bash  ")
    os.system(f"perl -p -i -e 's/{allnodes}/ {tips}/;' locus*txt")

def run_topic(topics,loci,seed, gaps=True):
    if gaps == False:
        os.system(f"python ~/topicmodel/TopicContml_project/topiccontml.py -gt rm_row -f . -nt {topics} -nl {loci} --threads 10")
        os.system(f"cp outtree outtree{loci}nogap-{seed}")
        os.system(f"python ~/topicmodel/TopicContml_project/topiccontml.py -f . -nt {topics} -nl {loci} -amb \"-\" --threads 10")
        os.system(f"cp outtree outtree{loci}nogkmer-{seed}")
    else:
        os.system(f"python ~/topicmodel/TopicContml_project/topiccontml.py -f . -nt {topics} -nl {loci} --threads 10")
        os.system(f"cp outtree outtree{loci}-{seed}")

if __name__ == '__main__':
    
    args = sys.argv[1:]
    treefile = args[0]
    reps     = args[1]
    rseed    = args[2]

    treestring = read_tree(treefile)
    run_dawg(treestring, rseed, reps)
    run_topic(5,reps,rseed)
