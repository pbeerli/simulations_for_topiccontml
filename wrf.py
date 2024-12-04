import numpy as np
import dendropy
from dendropy.calculate import treecompare
import time
import sys

# to use this the RUN_PARALLEL needs to be True
# but my other changes are actually faster so do not change
# RUN_PARALLEL
#from concurrent.futures import ThreadPoolExecutor, as_completed

RUN_PARALLEL = False

def run_wRF_pair1(t1,t2):  #unweighted
    t2.encode_bipartitions()
    d=treecompare.unweighted_robinson_foulds_distance(t1, t2, is_bipartitions_updated=True)
    return d

def run_wRF_pair2(t1,t2):    #weighted
    t2.encode_bipartitions()
    d=treecompare.weighted_robinson_foulds_distance(t1, t2, edge_weight_attr='length', is_bipartitions_updated=True)
    return d

def run_wRF_pair(a):
    t1,t2 = a
    t2.encode_bipartitions()
    d=treecompare.weighted_robinson_foulds_distance(t1, t2, edge_weight_attr='length', is_bipartitions_updated=True)
    return d

def process(tmptreelist):
    with ThreadPoolExecutor(max_workers=8) as executor:
        return  executor.map(run_wRF_pair, tmptreelist, timeout=60)

def RF_distances(n, filename_treelist, type="weighted"):
    tic1 = time.perf_counter()
    tns = dendropy.TaxonNamespace()
    distance_matrix=np.zeros((n,n))
    tlst = dendropy.TreeList(taxon_namespace=tns)
    if isinstance(filename_treelist,list):
        for f in filename_treelist:
            tlst.read(file=open(f,'r'),schema="newick")
        trees = tlst
    else:
        with open(filename_treelist, 'r') as f:
            trees=dendropy.Treelist.get(file=f,schema="newick",taxon_namespace=tns)
    toc1 = time.perf_counter()
    time1 = toc1 - tic1
#    print(f"Time of reading {n} trees= {time1}")
    
    tic2 = time.perf_counter()
    for i in range(1,n):
        trees[i].encode_bipartitions()
        t1 = trees[i]
        if RUN_PARALLEL:
            tmptreelist = [(trees[i],trees[j]) for j in range(i)]
            dlist = process(tmptreelist)
            distance_matrix[i][:i] = list(dlist)
        else:
            for j in range(i):
                #if type == "weighted":
                d1 = run_wRF_pair2(t1,trees[j])    #weighted
                #else:
                d2 = run_wRF_pair1(t1,trees[j])     #unweighted
                distance_matrix[i][j] = d1
                distance_matrix[j][i] = d2
    toc2 = time.perf_counter()
    time2 = toc2 - tic2
    print(f"Time of distance matrix of {n}-trees using {type}-RF = {time2}")
    return distance_matrix


if __name__ == "__main__":
    if len(sys.argv)>1:
        args = sys.argv[1:]
        n = len(args)
        outtreelist = args
        d = RF_distances(n, outtreelist)
        for di in d:
            for dj in di:
                print (f"{dj:3.4f}",end=' ')
            print()
        print()
        s = 0
        same = 0
        close2 = close4 = close6 = close8 = 0
        print("Distance to the true tree")
        for i in range(1,n):
            if d[0][i] == 0.0:
                same += 1
            if d[0][i] <= 2.0:
                close2 += 1
            if d[0][i] <= 4.0:
                close4 += 1
            if d[0][i] <= 6.0:
                close6 += 1
            if d[0][i] <= 8.0:
                close8 += 1
            s += d[i][0]
            print(d[0][i],d[i][0])
        print(f'RF={same}/{n-1},RF<=2,4,6,8:{close2/(n-1)} {close4/(n-1)} {close6/(n-1)} {close8/(n-1)}, mean(wRF)={s/(n-1)}')
    else:
        n = 11
        outtreelist = "outtrees"
        d = RF_distances(n, outtreelist)
        for di in d:
            for dj in di:
                print (f"{dj:3.4f}",end=' ')
            print()
        print()
    
