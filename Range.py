from NUM import NUM

class Range(NUM):
    def __init__(self):
        NUM.__init__(self)
        self.span = self.max - self.min

    def update(self,x):
        NUM.update(self,x)
        self.span = self.max - self.min

    def __str__(self):
        return "{\tspan = %f, lo = %f, n=%d, hi=%f\t}"%(self.span,self.min,int(self.n),self.max)

if __name__ == '__main__':
    r = Range()

    arr = [1, 2, 3, 444, 56]

    for x in arr:
        r.update(x)
    print r.arr, r.min, r.max, r.mean, r.sd, r.span
    print r.normalize(60)