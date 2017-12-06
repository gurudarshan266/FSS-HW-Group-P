import numpy as np
import random
import time
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import euclidean_distances
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.svm import SVC
from preprocess import preprocess
from ParamSet import ParamSet
import logging
import copy
import param_grid as pg
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from DE import DiffentialEvolutionTuner
import computation_config as cc
from sklearn.model_selection import KFold
from sklearn.model_selection import RepeatedKFold
from defines import *
import sys
import os
import ensembles
import best_param_ensemble

def compute_score(goal = "f1", Y_predict = None, Y_test = None):
    # Select the score based on the goal
    score = 0
    if goal == "accuracy":
        score = accuracy_score(Y_test, Y_predict)
    elif goal == "f1":
        score = f1_score(Y_test, Y_predict)
    elif goal == "precision":
        score = precision_score(Y_test, Y_predict)
    elif goal == "recall":
        score = recall_score(Y_test, Y_predict)
    elif goal == "auc" or goal == "roc_auc":
        score = roc_auc_score(Y_test, Y_predict)
    return score


def classify(learner, goal, X,Y,train,test):
    X_train = X.loc[train]
    X_test = X.loc[test]
    y_train = Y.loc[train]
    y_test = Y.loc[test]

    # Smote the data
    sm = SMOTE(random_state=SEED_SMOTE)
    X_train, y_train = sm.fit_sample(X_train, y_train)

    # Train the model
    learner.fit(X_train, y_train)

    # Predict the presence of bugs
    y_predicted = learner.predict(X_test)

    # Compute the score
    score = compute_score(goal=goal, Y_predict=y_predicted, Y_test=y_test)
    return score



def execute_cross_val(learner, goal, X, Y, k=5):
    results =[]
    random_state = 12883823
    rkf = RepeatedKFold(n_splits=k, n_repeats=k, random_state=random_state)
    # Run loop for 5x5 fold validation
    for train, test in rkf.split(X):
        score = classify(learner, goal, X, Y, train, test)
        results.append(score)
    return results


if __name__=='__main__':

    tune_ensemble = True

    goal = "accuracy"
    dataset = 'lucene'
    if len(sys.argv) > 1:
        dataset = sys.argv[1]

    results_base_dir = "../results/%s/"%goal

    k_file_name = results_base_dir+"%s.kout"%(dataset)
    k_file = open(k_file_name, "w+")

    results = {}
    run_times = {}
    header = "Learner|Best Params|Untuned Score|Tuned Score"

    with open(results_base_dir+"%s_results.csv"%dataset, "w+") as file:
        # Write the file header
        file.write(header+"\n")

        results[dataset] = {}
        for learner in cc.learners:
            print("DATASET = %s | LEARNER = %s"%(dataset,learner))

            # Get the parameter grid for the learner
            paramgrid = pg.param_grid[learner]

            # Get the learner object
            learner_obj = cc.learner_objs[learner]

            # Fetch training, tuning and testing datasets for the dataset
            X,Y = preprocess(dataset=dataset, do_smote = True)

            start_time = time.time()
            # Instantiate the tuner
            de_tuner = DiffentialEvolutionTuner(learner=learner_obj,param_grid=paramgrid,
                                                X_train=X['train'], Y_train=Y['train'],
                                                X_tune=X['tune'], Y_tune=Y['tune'],
                                                X_merged=X['merged'], Y_merged=Y['merged'],
                                                X_test=X['test'], Y_test=Y['test'],
                                                np=50, goal=goal, life=10, cr=0.8, f=0.5)


            # Run the tuner
            tuned_test_score, best_params, tune_score, untuned_test_score = de_tuner.tune_and_evaluate(n_DE=1)

            end_time = time.time()

            # Compute the time taken by the ensemble
            run_times[learner] = end_time - start_time
            # Save the resutls
            results[dataset][learner] = (best_params, untuned_test_score, tuned_test_score)

            # Write results to a file
            file.write("%s|%s|%f|%f\n"%(learner,best_params, untuned_test_score, tuned_test_score))
            file.flush()

            # Run 5x5 cross validation
            learner_obj.set_params(**best_params)
            k_scores = execute_cross_val(learner=learner_obj,
                                         goal=goal,
                                         X=X['test'], Y=Y['test'],
                                         k=5)

            # Write cross val results to file
            k_file.write("%s\n"%learner)
            k_scores_str = " ".join([str(x) for x in k_scores])
            k_file.write("%s\n\n"%k_scores_str)
            k_file.flush()


        k_file.close()
        print(run_times)

        # Run Scott-Knott test to get the learners ranks
        sk_ranks = {}
        sk_out = os.popen('cat %s | python SK.py'%k_file_name)
        sk_out = sk_out.readlines()[3:] # output starts from line 4
        for line in sk_out:
            line = line.split(",")
            line = [ x.strip() for x in line]
            sk_ranks[line[1]] = int(line[0])


        # Tune ensemble learner
        if tune_ensemble:
            learner = 'tuned_ensemble'
            print("DATASET = %s | LEARNER = %s" % (dataset, learner))
            print(sk_ranks)

            start_time = time.time()

            # Get the tuned scores
            tuned_test_score, best_params, tune_score, untuned_test_score = \
                ensembles.ensemble_tune(goal=goal,dataset=dataset,sk_ranks=sk_ranks)

            end_time = time.time()

            run_times[learner] = end_time-start_time

            best_params_to_print = {}
            for k in best_params:
                if '__' in k:
                    best_params_to_print[k] = best_params[k]
            # Write results to file
            file.write("%s|%s|%f|%f\n" % (learner, best_params_to_print, untuned_test_score, tuned_test_score))
            file.flush()

            results[dataset][learner] = (best_params_to_print, untuned_test_score, tuned_test_score)


            # Best param ensemble
            learner = 'best_param_ensemble'
            best_param_score = best_param_ensemble.tune_best_param_ensembles(goal=goal, dataset=dataset, best_params=results,sk_ranks=sk_ranks)
            best_param_untuned_score = results[dataset]["tuned_ensemble"][1]
            # Write results to file
            file.write("%s|%s|%f|%f\n" % (learner, {}, best_param_untuned_score, best_param_score))
            file.flush()

            results[dataset][learner] = ({}, best_param_untuned_score, best_param_score)

        file.write("\n\nTuning Times:\n")
        file.write(str(run_times))
        file.flush()


    # Dump the python dictionary to a file
    with open(results_base_dir+"%s_tune.py"%(dataset),"w+") as res_file:
        res_file.write(str(results))
    print(results)
    print(run_times)


