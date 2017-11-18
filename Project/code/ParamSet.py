import copy

class ParamSet:
    def __init__(self, params = None):
        if params is not None:
            self.params = params
        else:
            self.params = {}
        self.score = None

    def clone(self):
        p = copy.deepcopy(self)
        p.score = None
        return p

    def __getitem__(self, index):
        return self.params[index]

    def __setitem__(self, key, value):
        self.params[key] = value

    def __contains__(self, value):
        return value in self.params

    def __len__(self):
        return len(self.params)

    def __str__(self):
        return str(self.params)+" | Score = "+self.score