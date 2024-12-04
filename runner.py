#!/usr/bin/env python
#
# runner for dawg simulations
import os
import sys
import simrun as si
import random

treefile = sys.argv[2]
loci     = int(sys.argv[1])
topics = 5

treestring = si.read_tree(treefile)

for i in range(10):
    rseed = random.randint(111,999999)
    os.system("rm simdata*")
    si.run_dawg(treestring, rseed, loci)
    si.run_topic(topics,loci,rseed,gaps=True)
    si.run_topic(topics,loci,rseed,gaps=False)
