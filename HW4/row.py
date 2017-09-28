class Row:

    def __init__(self, data, goals_index, weights, id=None):
        self.cells = data
        self.goals_index = goals_index
        self.weights = weights
        self.id = id

    def __str__(self):
        return ", ".join([ str(x) for x in self.cells])