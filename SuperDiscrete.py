from NUM import NUM
from SYM import SYM
from Range import Range
import math
import UDiscrete
import copy
import sys

def SupervisedDiscrete(things,x=None,y=None,nump=True,lessp=True):
    y = y or (lambda p:p[-1])
    x = x or (lambda p:p[0])
    better = lessp and (lambda p,q:  p<q) or (lambda p,q:  p>q)
    what = nump and NUM or SYM
    compute_spread = nump and (lambda num: num.sd)
    break_points = {}
    ranges = UDiscrete.UDiscretize(things,x)
    ranges = [None]+ranges

    def data(j):
        return ranges[j].arr

    def memo(here,stop, _memo, b4=None, inc=None):
        b4 = b4 or NUM()
        inc = 1 if stop > here else -1
        if here != stop:
            b4 = copy.deepcopy(memo(here+inc,stop, _memo))
        b4.updates(data(here), y)
        _memo[here] = b4
        return _memo[here]

    def combine(low, high, all, bin_, lvl):
        best = compute_spread(all)
        lmemo = {}
        rmemo = {}

        memo(high, low, lmemo)
        memo(low, high, rmemo)

        cut, rbest, lbest=None,0.0,0.0

        for j in range(low, high):
            l = lmemo[j]
            r = rmemo[j+1]

            tmp = l.n/all.n*compute_spread(l) + r.n/all.n*compute_spread(r)
            if better(tmp, best):
                cut = j
                best = tmp
                lbest = copy.deepcopy(l)
                rbest = copy.deepcopy(r)

        if cut  :
            bin_ = combine(low, cut, lbest, bin_, lvl + 1) + 1
            bin_ = combine(cut + 1, high, rbest, bin_, lvl + 1)
        else:
            if bin_ not in break_points:
                break_points[bin_] = -1e-32
            if ranges[high].num.max > break_points[bin_]:
                break_points[bin_] = ranges[high].num.max

        return bin_

    combine(1, len(ranges)-1, memo(1,len(ranges)-1,{}), 1, 0)
    return break_points



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

    breaks = SupervisedDiscrete(table, lambda p:float(p[0]) , lambda p:float(p[-1] ) )
    print "\nSupervised Discretizer:"
    for k in breaks:
        print "super\t%s\t{ label = %s, most = %f}"%(str(k),str(k),breaks[k])




