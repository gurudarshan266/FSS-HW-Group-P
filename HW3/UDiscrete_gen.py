import random
import sys

N = 50

def klass(x):
    global N
    if x < 0.2:
        return 0.2 + random.random()/N
    elif x < 0.6:
        return 0.6 + random.random()/N
    else:
        return 0.9 + random.random()/N

if __name__ == '__main__':
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    print "#Samples = %d"%N

    #random.seed(random.randint(0,1000))
    with open("UD_sample.txt","w+") as fp:
        for i in range(N):
            x = random.random()
            y = klass(x)
            fp.write("%f %f\n"%(x,y))
