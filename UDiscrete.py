import sys
import math
from helpers import *
from Range import Range
from NUM import NUM


def update(arr):
    num_arr = NUM.createNUM(arr)
    N = len(arr)
    bin_size = math.floor(math.sqrt(N))
    epsilon = 0.1*num_arr.sd

    print "SD = %f"%num_arr.sd
    print  "bin size = %d"%int(bin_size)
    print "Epsilon = %f"%epsilon

    bins = []
    r = Range()
    last = -float("inf")
    last_range_max = 0.0

    r.update(arr[0])
    last = arr[0]
    for i in range(1,len(arr)):
        x = arr[i]

        if x > last and \
                        r.span > epsilon and \
                r.n >= bin_size and \
                x - last_range_max > epsilon:
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
            if isFloat(line):
                arr.append(float(line))

    # Sort the array
    arr.sort()

    print arr
    bins = update(arr)
    print bins
    for bin in bins:
        print bin



