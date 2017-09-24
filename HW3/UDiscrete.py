import sys
import math

sys.path.append("../common")

from helpers import *
from Range import Range
from NUM import NUM


def update(arr,f=None):
    f = f or (lambda x:x[0])
    x0_arr = [f(row) for row in arr]
    num_arr = NUM.createNUM(x0_arr)
    N = len(arr)
    bin_size = math.floor(math.sqrt(N))
    epsilon = 0.2*num_arr.sd

    # print "SD = %f"%num_arr.sd
    # print  "bin size = %d"%int(bin_size)
    # print "Epsilon = %f"%epsilon

    bins = []
    r = Range()
    last = -float("inf")
    last_range_max = 0.0

    r.update(arr[0],f)
    last = f(arr[0])
    for i in range(1,len(arr)):
        x = f(arr[i])

        if      x > last and \
                r.num.get_span() > epsilon and \
                r.n > bin_size and \
                num_arr.n - i > bin_size and \
                num_arr.max - x > epsilon and \
                len(bins)<bin_size-1:
            # add the Range object to the bins array
            bins.append(r)
            last_range_max = r.num.max
            # Create a new Range (bin)
            r = Range()

        # Add the value to the range
        r.update(arr[i],f)
        last = x
    bins.append(r)
    return bins


# t is the table
# x is the function used to extract the data
def UDiscretize2(t,x=None):
    x = x or (lambda p: p[0])
    arr = []
    for row in t:
        val = x(row)
        if isFloat(val):
            arr.append(float(val))
    print arr
    # Sort the array
    arr.sort()
    bins = update(arr)
    print "\nUnsupervised discretization:"
    for i in range(len(bins)):
        print "x\t%d\t%s" % (i + 1, bins[i])

    return bins

# t is the table
# x is the function used to extract the data
def UDiscretize(t, x=None):
    x = x or (lambda p: p[0])
    #print t
    # Sort the array
    t.sort(key=lambda p: x(p))
    bins = update(t,x)
    print "\nUnsupervised discretization:"
    for i in range(len(bins)):
        print "x\t%d\t%s" % (i + 1, bins[i])

    return bins

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

    #print bins
    bins = UDiscretize(table, lambda p: float(p[0]) )




