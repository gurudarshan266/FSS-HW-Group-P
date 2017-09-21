import sys
import math
from helpers import *
from Range import Range
from NUM import NUM


def update(arr):
    num_arr = NUM.createNUM(arr)
    N = len(arr)
    bin_size = math.floor(math.sqrt(N))
    epsilon = 0.2*num_arr.sd

    print "SD = %f"%num_arr.sd
    print  "bin size = %d"%int(bin_size)
    print "Epsilon = %f"%epsilon

    bins = []
    r = Range()
    last = -float("inf")
    last_range_max = 0.0

    r.update(arr[N-1])
    last = arr[N-1]
    for i in range(1,len(arr)):
        x = arr[N-i-1]

        if x < last and \
                        r.span > epsilon and \
                r.n > bin_size and \
                r.max - x > epsilon and len(bins)<bin_size-1:
            # add the Range object to the bins array
            bins.append(r)
            last_range_max = r.max
            # Create a new Range (bin)
            r = Range()

        # Add the value to the range
        r.update(x)
        last = x
    bins.append(r)
    return bins



if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Usage: \n %s <file>" % (sys.argv[0])
        sys.exit(-1)

    arr = []

    in_file = sys.argv[1]

    # Extract the file data into array
    with open(in_file, "r") as fp:
        for line in fp:
            line = line.strip()
            x,y = line.split()[:2]
            if isFloat(x):
                arr.append(float(x))

    # Sort the array
    arr.sort()

    print arr
    bins = update(arr)
    print bins
    for bin in bins:
        print bin



