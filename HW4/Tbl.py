import sys
sys.path.append("../common")
sys.path.append("../HW3")

import math
import operator
import copy

from defines import *
from row import Row
from NUM import NUM
from SYM import SYM
from SuperDiscrete import SupervisedDiscrete

def isfloat(val):
    try:
        float(val)
        return True
    except:
        return False

class Tbl:

    def __init__(self, header_str):
        self.orig_header_str = header_str
        line_split = header_str.split(',')
        self.headers = [x.strip() for x in line_split]

        self.funs={"dom":self.dom}

        self.datatype_matrix = []
        self.weights = []
        self.goals_index = []
        self.Rows = []
        self.containers = []
        self.x = {"syms":[], "nums":[], "cols":[]} # all independent columns
        self.y = {"syms":[], "nums":[], "cols":[]} # all dependent columns
        self.all = {"syms": [], "nums": [], "cols": []} # all columns
        self.less = []
        self.more = []
        self.goals = []
        self.dom_scores = {}

        for i in range(len(self.headers)):
            x = self.headers[i]

            if x.startswith('?'):
                self.datatype_matrix.append(DataType.IGNORE)
                self.weights.append(0)
                self.containers.append(None)
                # TODO: check if it has to added to self.all["cols"]
                self.all["cols"].append(None)


            elif x.startswith('$') or x.startswith('%'):
                self.datatype_matrix.append(DataType.NUMBER)
                self.weights.append(1)
                # add to respective groups
                cont = NUM(pos=i,txt=x)
                self.containers.append(cont)
                self.all["cols"].append(cont)
                self.x["cols"].append(cont)
                self.all["nums"].append(cont)
                self.x["nums"].append(cont)


            elif x.startswith('<'):
                self.datatype_matrix.append(DataType.NUMBER|DataType.MIN_GOAL)
                self.weights.append(-1)
                self.goals_index.append(i)
                # add to respective groups
                cont = NUM(pos=i,txt=x)
                self.containers.append(NUM())
                self.all["cols"].append(cont)
                self.y["cols"].append(cont)
                self.all["nums"].append(cont)
                self.goals.append(cont)
                self.less.append(cont)
                self.y["nums"].append(cont)


            elif x.startswith('>'):
                self.datatype_matrix.append(DataType.NUMBER|DataType.MAX_GOAL)
                self.weights.append(1)
                self.goals_index.append(i)
                # add to respective groups
                cont = NUM(pos=i,txt=x)
                self.containers.append(NUM())
                self.all["cols"].append(cont)
                self.y["cols"].append(cont)
                self.all["nums"].append(cont)
                self.goals.append(cont)
                self.more.append(cont)
                self.y["nums"].append(cont)


            elif x.startswith('!'):
                self.datatype_matrix.append(DataType.SYMBOL)
                self.weights.append(1)
                # add to respective groups
                cont = SYM(pos=i,txt=x)
                self.containers.append(cont)
                self.all["cols"].append(cont)
                self.y["syms"].append(cont)
                self.y["cols"].append(cont)
                self.all["syms"].append(cont)


            else:
                self.datatype_matrix.append(DataType.SYMBOL)
                self.weights.append(1)
                # add to respective groups
                cont = SYM(pos=i,txt=x)
                self.containers.append(cont)
                self.all["cols"].append(cont)
                self.x["cols"].append(cont)
                self.all["syms"].append(cont)
                self.x["syms"].append(cont)


    def parse_val(self,s):
        ''' Attempt to convert the string to float. Return the string, if it fails'''
        try:
            x = float(s)
            return x
        except:
            return s

    def is_acceptable_row(self, row):
        ''' Check if the given row contains valid data '''

        for i in range(len(row)):
            x = row[i]

            if self.datatype_matrix[i] & 0x3 == DataType.IGNORE:
                continue

            if isfloat(x):
                continue

            if not isfloat(x) and self.datatype_matrix[i] & 0x3 != DataType.SYMBOL:
                return False
        return True

    def add_row(self,line):
        vals = []
        if type(line) == str:
            line_split = line.split(',')

            # Print error message if the number of columns are mismatching
            if len(line_split) != len(self.headers):
                return None

            # print line
            for i in range(len(line_split)):
                val = self.parse_val(line_split[i].strip())
                vals.append(val)

            if not self.is_acceptable_row(vals):
                return

        else:
            vals = line.cells

        # Update the containers
        for i in range(len(vals)):
            if self.datatype_matrix[i]&0x3 != DataType.IGNORE:
                self.containers[i].update(vals[i])

        r = Row(vals,self.goals_index,self.weights, id =len(self.Rows))
        self.Rows.append(r)
        return r


    def dominate1(self,i,j):
        e = 2.71828
        n = len(self.goals_index)
        sum1 = 0.0
        sum2 = 0.0

        for index in self.goals_index:
            w = self.weights[index]
            container = self.containers[index]
           # print "(%d,%d)"%(i,j)
            x = container.normalize(self.Rows[i].cells[index])
            y = container.normalize(self.Rows[j].cells[index])
            sum1 = sum1 - math.pow(e,(1.0*w*(x-y))/n)
            sum2 = sum2 - math.pow(e,(1.0*w*(y-x))/n)

        return sum1/n < sum2/n


    def dominate_score(self,i):
        count = 0
        for j in range(len(self.Rows)):
            if i != j:
                if self.dominate1(i,j):
                    count = count + 1
        return count

    def compute_domination_scores(self):
        scores = {}
        for i in range(len(self.Rows)):
            scores[i]=(self.dominate_score(i))
        return scores

    def get_sorted_indices(self):
        scores = self.compute_domination_scores()
        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
        return sorted_scores

    def copy(self, frm):
        j = Tbl(self.orig_header_str) # Create a new table with the same set of headers

        for r in frm:
            j.add_row(r)
        return j


    def discretizeHeaders(self):
        return [ (s.replace("$","")).replace("%","") for s in self.headers]

    def dom(self, r):
        if r.id not in self.dom_scores:
            self.dom_scores[r.id] = self.dominate_score(r.id)
        return self.dom_scores[r.id]

    def  data(self, cells, old):
        new = self.add_row(",".join([str(x) for x in cells]))#Row(cells, self.goals_index, self.weights)
        if old:
            new.id = old.id
        return new


    def discretizeRows(self, y=None):
        disc_headers = self.discretizeHeaders()
        disc_headers_str = ",".join(disc_headers)
        j = Tbl(disc_headers_str)

        #TODO: Hardcoded to return dom score for HW4, add new functions
        yfunc = self.funs["dom"]

        for head in (self.x["nums"]):
            cooked = (j.all["cols"])[head.pos]
            x = lambda r: r.cells[cooked.pos]
            cooked.bins = SupervisedDiscrete(self.Rows,x,yfunc)
        for r in (self.Rows):
            tmp = copy.deepcopy(r.cells)
            for head in self.x["nums"]:
                cooked = (j.all["cols"])[head.pos]
                old = tmp[cooked.pos]
                new = SYM.discretize(cooked,old)
                tmp[cooked.pos] = new
            j.data(tmp,r)
        return j


