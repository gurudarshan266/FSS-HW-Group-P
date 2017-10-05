import sys
sys.path.append("../common")

import copy
from NUM import NUM

def has(branch):
    out = []
    for i in branch:
        step = branch[i] if type(branch)==dict else i
        x ={"attr":step["attr"] , "val":step["val"]}
        step["has"] = x
        out.append(x)
    return out

def have(branches):
    for k in branches:
        branch = branches[k] if type(branches)== dict else k
       # branch[0]["has"] = has(branch)
        has(branch)
    return branches


def branches1(tr,out,b):
    if tr["attr"]:
        b.append( {"attr":tr["attr"], "val":tr["val"], "_stats":tr["stats"]})
    if len(b) > 0:
        out.append(b)

    for kid in tr["_kids"]:
        #kid = tr["_kids"][k]
        branches1(kid,out, copy.deepcopy(b))
    return out

def branches(tr):
    return have(branches1(tr,[],[]))

def member2(twin0, twins):
    for k in twins: # could be list
        twin1 = twins[k]
        if twin0["attr"] == twin1["attr"] and twin0["val"]==twin1["val"]:
            return True
    return False

def delta(t1, t2):
    out = []
    for k in t1: # could be list
        twin = t1[k]
        if not member2(twin,t2):
            out.append([twin["attr"],twin["val"]])
    return out


def contrasts(branches, better):
    for i in range(len(branches)):
        branch1 = branches[i]
        out = []
        for j in range(len(branches)):
            branch2 = branches[j]
            if i!= j:
                num1 = branch1[-1]["_stats"]
                num2 = branch2[-1]["_stats"]
                if better(num2.mean,num1.mean):
                    if not NUM.same(num1, num2): # to be implemented
                        inc = delta(branch2["has"],branch1["has"])

                        if len(inc) > 0:
                            out.append({"i":i,"j":j, "ninc":len(inc), "muinc":num2.mean - num1.mean, "inc":inc, "branch1":branch1["has"], "mu1":num1.mean, "branch2":branch2["has"], "mu2":num2.mean})


        if len(out)>0:
            print()
            out.sort(key=lambda x:-x["muinc"])
            print(i,"max mu ",out[0])
            out.sort(key=lambda x:x["ninc"])
            print(i,"min inc ",out[0])

def more(x,y):
    return x>y

def less(x,y):
    return x<y

def plans(branches):
    return contrasts(branches,more)

def monitors(branches):
    return contrasts(branches,less)