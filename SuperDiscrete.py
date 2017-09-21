from NUM import NUM
from SYM import SYM
from Range import Range
import math
import UDiscrete
import copy
import sys

def SupervisedDiscrete(things,x=None,y=None,nump=None,lessp=None):
    y = y or (lambda p:p[-1])
    nump = nump==None and True or nump
    lessp = lessp==None and True or lessp

    better = lessp and (lambda p,q:  p<q) or (lambda p,q:  p>q)
    what = nump and NUM or SYM
    z = nump and (lambda num: num.sd)
    breaks = {}
    ranges = UDiscrete.UDiscretize(things,x)
    ranges = [None]+ranges

    def data(j):
        return ranges[j].arr

    def memo(here,stop, _memo, b4=None, inc=None):
        b4 = b4 or Range()
        inc = 1 if stop > here else -1
        if here != stop:
            b4 = copy.deepcopy(memo(here+inc,stop, _memo))
        b4.updates(data(here))
        _memo[here] = b4
        return _memo[here]

    def combine(lo, hi, all, bin, lvl):
        best = z(all)
        lmemo = {}
        rmemo = {}

        memo(hi, lo, lmemo)
        memo(lo, hi, rmemo)

        cut,rbest,lbest=None,0.0,0.0

        for j in range(lo,hi):
            l = lmemo[j]
            r = rmemo[j+1]

            tmp = l.n/all.n*z(l) + r.n/all.n*z(r)
            if better(tmp, best):
                cut = j
                best = tmp
                lbest = copy.deepcopy(l)
                rbest = copy.deepcopy(r)

        bin = 0

        if cut!=None :
            bin = combine(lo, cut, lbest, bin, lvl+1)+1
            bin = combine(cut+1, hi, rbest, bin, lvl+1)
        else:
            if bin not in breaks:
                breaks[bin] = -1e-32
            if ranges[hi].max > breaks[bin]:
                breaks[bin] = ranges[hi].max

        return bin

    combine(1, len(ranges)-1, memo(1,len(ranges)-1,{}), 1, 0)
    return breaks



if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Usage: \n %s <file>" % (sys.argv[0])
        sys.exit(-1)

    table = []

    in_file = sys.argv[1]

    # Extract the file data into array
    with open(in_file, "r") as fp:
        for line in fp:
            line = line.strip()
            table.append(line.split())

    breaks = SupervisedDiscrete(table,(lambda p:p[0]),(lambda p:p[1]))
    print "\nSupervised Discretizer:"
    for k in breaks:
        print "super\t%s\t{ label = %s, most = %f}"%(str(k),str(k),breaks[k])




