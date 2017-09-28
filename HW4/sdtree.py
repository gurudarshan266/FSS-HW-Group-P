import sys
sys.path.append("../common")
sys.path.append("../HW3")

from NUM import NUM
from helpers import *
from Tbl import Tbl
import copy

tree_min = 2 #TODO: reverify the values
tree_max_depth = 100

def create(t, yfun, pos, attr, val):
    s = NUM()
    s.updates(t.Rows,yfun)
    return { "_t" :t, "_kids" : [], "yfun": yfun, "pos":pos, "attr":attr,"val":val, "stats" : s}

def order (t,y):
    # col = list of nums for the rows
    def xpect(col):
        tmp = 0
        for x in col.nums:
            tmp = tmp + (x.sd*x.n*1.0)/len(col) #recheck the order of multiply and divide
        return tmp

    def whatif(head,y):
        col = {"pos":head.pos, "what":head.txt, "nums":{}, "n":0}
        for row in (t.Rows): # t.rows = list of all the rows in the table
            x = row.cells[col["pos"]]
            if isFloat(x):
                col["n"] = col["n"] + 1

                if x not in col["nums"]:
                    col["nums"][x] = NUM()
                col["nums"][x].update(y(row))
        return {"key":xpect(col),"val":col}

    out = []

    for h in t.x["cols"]:
        out.append(whatif(h,y))
    out.sort(key=lambda x: x["key"])

    return [ x["val"] for x in out]

def grow1(above,yfun,rows,lvl,b4,pos = None,attr = None,val = None):
    def pad(): return "%-20s"%("| "*lvl)

    def likeAbove(): return above["_t"].copy(rows)

    if len(rows) >= tree_min:
        if lvl <= tree_max_depth:
            here = (lvl==0) and above or create(likeAbove(), yfun, pos, attr, val)
            if here["stats"].sd < b4:
                if lvl > 0:
                    above["_kids"].append(here)
                cuts = order(here["_t"], yfun)
                cut = cuts[0]
                kids = []
                for r in rows:
                    val = r.cells[cut["pos"]]
                    if isFloat(val):
                        rows1 = kids[val] or []
                        rows1.append(r)
                        kids[val] = rows1
                for val,rows1 in enumerate(kids):
                    if len(rows1) < len(rows):
                        grow1(here,yfun,rows1,lvl+1,here["stats"].sd,cut["pos"],cut["what"],val)

def grow(t,y):
    yfun = t.dom # hardcoded to dom
    root = create(t, yfun)
    grow1(root,yfun,t.Rows, 0, 1e32)
    return root

def tprint(tr, lvl=None):
    def pad(): return '| '*(lvl-1)
    def left(x): return "%-20s"%x
    lvl = lvl or 0
    suffix=""
    if len(tr["kids"])==0 or lvl ==0:
        suffix = "n=%s mu=%-.2f sd=%-.2f"%(tr["stats"].n, tr["stats"].mu, tr["stats"].sd)

    if lvl == 0:
        print "\n"+suffix
    else:
        print left(pad()) + tr["attr"] or "" + tr["val"] or "" + "\t:" + suffix
    for j in range(len(tr["_kids"])):
        tprint( (tr["_kids"])[j], lvl +1)

def leaf(tr, cells, bins, lvl=None):
    lvl = lvl or 0
    for j,kid in enumerate(tr["_kids"]):
        pos,val = kid["pos"],kid["val"]
        if cells[kid["pos"]] == kid["val"]:
            return leaf(kid, cells, bins, lvl+1)
    return tr

