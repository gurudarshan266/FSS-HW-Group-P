import sys
sys.path.append("../common")

import copy
from NUM import NUM

def has(branch):
    out = []
    for i in branch:
        step = branch[i]
        out.append({"attr":step["attr"] , "val":step["val"]})
    return out

def have(branches):
    for k in branches:
        branch = branches[k]
        branch["has"] = has(branch)
    return branches


def branches1(tr,out,b):
    if tr["attr"]:
        b.append( {"attr":tr["attr"], "val":tr["val"], "_stats":tr["stats"]})
    if len(b) > 0:
        out.append(b)

    for k in tr["_kids"]:
        kid = tr["_kids"][k]
        branches1(kid,out, copy.deepcopy(b))
    return out

def branches(tr):
    return have(branches1(tr,[],[]))

def member2(twin0, twins):
    for k in twins:
        twin1 = twins[k]
        if twin0["attr"] == twin1["attr"] and twin0["val"]==twin1["val"]:
            return True
    return False

def delta(t1, t2):
    out = []
    for k in t1:
        twin = t1[k]
        if not member2(twin,t2):
            out.append([twin["attr"],twin["val"]])
    return out


def contrasts(branches, better):
    for i in branches:
        branch1 = branches[i]
        out = []
        for j in branches:
            branch2 = branches[j]
            if i!= j:
                num1 = branch1[sorted(branch1.keys())[-1]]["_stats"]
                num2 = branch2[sorted(branch1.keys())[-1]]["_stats"]
                if better(num2.mu,num1.mu):
                    if not NUM.same(num1, num2): # to be implemented
                        inc = delta(branch2["has"],branch1["has"])

                        if len(inc) > 0:
                            out.append({"i":i,"j":j, "ninc":len(inc), "muinc":num2.mean - num1.mean, "inc":inc, "branch1":branch1["has"], "mu1":num1.mean, "branch2":branch2["has"], "mu2":num2.mean})


        print()
        out.sort(key=lambda x:-x["muinc"])
        print(i,"max mu ",out[1])
        out.sort(key=lambda x:x["ninc"])
        print(i,"min inc ",out[1])

