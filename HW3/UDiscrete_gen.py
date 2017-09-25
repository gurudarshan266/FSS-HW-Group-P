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

def klass2(x):
    global N
    if x < 0.2:
        return "CAT"
    elif x < 0.6:
        return "DOG"
    else:
        return "WOLF"

if __name__ == '__main__':
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    print "#Samples = %d"%N

    gen_sym = len(sys.argv) > 2 and (sys.argv[2]=='SYM' or sys.argv[2]=='Sym' or sys.argv[2]=='sym')

    klass_func = klass if not gen_sym else klass2

    #random.seed(random.randint(0,1000))
    with open("UD_sample.txt","w+") as fp:
        for i in range(N):
            x = random.random()
            y = klass_func(x)
            fp.write("%f %s\n"%(x,y))
