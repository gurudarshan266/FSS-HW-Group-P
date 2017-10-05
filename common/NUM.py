import math

num_small = 0.38
num_first = 3
num_last = 96
num_criticals = {95:{3:3.182, 6:2.447, 12:2.179, 24:2.064, 48:2.011, 96:1.985},\
                 99:{3:5.841, 6:3.707, 12:3.055, 24:2.797, 48:2.682, 96:2.625}}
num_conf = 95

class NUM:
    'Used for NUMS manipulation'

    def __init__(self,pos=0,txt=""):
        self.min = float('inf')
        self.max = -float('inf')
        self.arr = []
        self.mean = 0.0
        self.m2 = 0
        self.sd = 0.0
        self.n = 0
        self.pos = pos
        self.bins = None
        self.txt = txt

    def __str__(self):
        return "%s POS = %d"%(self.txt, self.pos)


    @classmethod
    def createNUM(cls,arr):
        num = NUM()
        for x in arr:
            num.update(x)
        return num

    def get_span(self):
        return self.max-self.min

    def update(self, row,f=None):
        f = f or (lambda val:val)
        x = f(row)
        x = float(x)
        self.arr.append(x)
        self.max = max(self.max, x)
        self.min = min(self.min, x)

        self.n = len(self.arr)
        n = self.n*1.0

        old_mean = self.mean
        delta = (x - old_mean)*1.0

        self.mean = (old_mean * 1.0) + (delta/ n)

        self.m2 = self.m2 + delta*(x-self.mean)

        if self.n > 1:
            self.sd = math.sqrt(self.m2/(self.n-1))*1.0

        #variance = (((n - 1) * self.sd * self.sd) + (x - old_mean) * (x - self.mean)) / n

        #self.sd = math.sqrt(variance) * 1.0

    def updates(self, rows, f=None):
        f = f or (lambda p:p)
        for row in rows:
            self.update(row,f)

    def normalize(self, x):
        y = ((x - self.min) * 1.0) / (self.max - self.min + 1e-32)
        return y

    @classmethod
    def hedges(cls,i,j):
        nom = (i.n-1.0)*(i.sd**2) + (j.n - 1.0)*(j.sd**2)*1.0
        denom = (i.n - 1.0) + (j.n - 1.0)
        sp = 0.0 + (nom/denom)**0.5
        g = abs(i.mean-j.mean)/sp
        c = 1.0-3.0/(4.0*(i.n + j.n - 2.0) - 1)
        return g*c > num_small

    @classmethod
    def ttest1(cls, df, first, last, crit):
        if df <= first:
            return crit[first]
        elif df >= last:
            return crit[last]
        else:
            n1 = first
            while n1 < last:
                n2 = n1*2.0
                if df >= n1 and df <= n2:
                    old,new = crit[n1], crit[n2]
                    return 0.0 + old + (new-old)*(df-n1+0.0)/(n2-n1+0.0)
                n1 = n1*2

    @classmethod
    def ttest(cls,i,j):
        t = (i.mean - j.mean + 0.0)/math.sqrt(max(1e-64, (i.sd**2 + 0.0)/i.n + (j.sd**2 + 0.0)/j.n ))
        a= (1.0*i.sd**2)/i.n
        b= (1.0*j.sd*2)/j.n
        df = (a+b+0.0)**2/(1e-64 + a**2/(i.n -1.0) + b**2/(j.n - 1.0))
        c= NUM.ttest1(math.floor(df+0.5), num_first, num_last, num_criticals[num_conf])
        return abs(t) > c

    @classmethod
    def same(cls,i,j):
        return not (NUM.hedges(i,j) and NUM.ttest(i,j))


if __name__ == '__main__':
    num = NUM()

    arr = [1, 2, 444, 56]

    for x in arr:
        num.update(x)
    print num.arr, num.min, num.max, num.mean, num.sd
    print num.normalize(60)
