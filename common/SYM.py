import math


class SYM:
    def __init__(self):
        self.counter = {}
        self.n = 0

    def update(self, s,f=None):
        f = f or (lambda s:str(s))
        s = str(f(s))
        if s not in self.counter:
            self.counter[s] = 0
        self.counter[s] = self.counter[s] + 1
        self.n = self.n + 1

    def entropy(self):
        if self.n == 0 :
            return 0
        e = 0.0
        for k in self.counter:
            v = self.counter[k]*1.0
            p = (v*1.0)/self.n
            e = e - p*math.log(p,2)
        return e

    def distance(x,y):
        return 0 if x==y else 1

    def updates(self,rows,f):
        for row in rows:
            s = str(f(row))
            self.update(s,f)



if __name__ == '__main__':
    sym = SYM()
    arr = ['A', 'B', 'B', 'B', 'B', 'C', 'C', 'C']

    for s in arr:
        sym.update(s)

    print sym.entropy()