import math


class NUM:
    'Used for NUMS manipulation'

    def __init__(self,pos=0):
        self.min = float('inf')
        self.max = -float('inf')
        self.arr = []
        self.mean = 0.0
        self.m2 = 0
        self.sd = 0.0
        self.n = 0
        self.pos = pos
        self.bins = []


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


if __name__ == '__main__':
    num = NUM()

    arr = [1, 2, 444, 56]

    for x in arr:
        num.update(x)
    print num.arr, num.min, num.max, num.mean, num.sd
    print num.normalize(60)
