from NUM import NUM

class Range:
    def __init__(self):
        self.num = NUM()
        self.span = self.num.max - self.num.min
        self.arr=[]
        self.n = 0

    def update(self, row, f=None):
        f = f or (lambda val : val)
        self.num.update(f(row))
        self.span = self.num.max - self.num.min
        self.arr.append(row)
        self.n = len(self.arr)

    def __str__(self):
        return "{\tspan = %f, lo = %f, n=%d, hi=%f\t}"%(self.span,self.num.min,len(self.arr),self.num.max)

if __name__ == '__main__':
    r = Range()

    arr = [1, 2, 3, 444, 56]

    for x in arr:
        r.update(x)
    print r.arr, r.num.min, r.num.max, r.num.mean, r.num.sd, r.num.get_span()
    print r.num.normalize(60)