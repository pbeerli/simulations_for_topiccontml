#!/usr/bin/env python
#
import os
import sys
replicates = 0
replicatesend = 100
NE = sys.argv[1]    #population size scaled by mu for example 0.01 <--> 4Ne*mu
tmrca = sys.argv[2] #time to the most recent common ancestor scaled in coalescent units [ms]
loci = sys.argv[3]  # number of loci
for i in range(replicates,replicatesend):
    addon=str(i)+"_"+NE+"_"+tmrca+"_"+loci
    infile = "infile_"+addon
    log = "log_"+addon
    halftmrca = str(float(tmrca)/2.0)
    os.system("python manyloci.py ./ms 40 "+loci+" -t "+NE+" -r 0 1000 -I 4 10 10 10 10 0.0 -n 1 0.25 -n 2 0.25 -n 3 0.25 -n 4 0.25 -T -M -q 1000 -ej "+halftmrca+"  3 1 -ej "+halftmrca+"  4 2 -eN "+halftmrca+" 0.5 -ej "+tmrca+"  2 1 -eN "+tmrca+" 1.0 > tree; migdata --modern < tree; cp infile "+infile)
