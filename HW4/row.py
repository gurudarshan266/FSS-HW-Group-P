class Row:

    def __init__(self, data, goals_index, weights, id=-1):
        self.cells = data
        self.goals_index = goals_index
        self.weights = weights
        self.id = id

    def __str__(self):
        return "ID=%d [%s]"%(self.id,", ".join([ str(x) for x in self.cells]))