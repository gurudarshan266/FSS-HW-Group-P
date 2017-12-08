import matplotlib.pyplot as plt
import scikitplot as skplt
import computation_config as cc

def plot_scores(goal='f1', dataset='lucene', results=None):
    plot_name = "%s_%s_plot"%(goal,dataset)

    learners = cc.learners + ['tuned_ensemble','best_param_ensemble']
    tuned_scores = []
    untuned_scores = []
    for learner in learners:
        tuned_score = results[goal][dataset][learner][2]
        untuned_score = results[goal][dataset][learner][1]




