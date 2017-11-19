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

    goal = "f1"
    dataset = 'jedit1'
    if len(sys.argv) > 1:
        dataset = sys.argv[1]

    results_base_dir = "../results/%s/"%goal

    k_file = open(results_base_dir+"%s.kout"%(dataset), "w+")

    results = {}
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

            # Instantiate the tuner
            de_tuner = DiffentialEvolutionTuner(learner=learner_obj,param_grid=paramgrid,
                                                X_train=X['train'], Y_train=Y['train'],
                                                X_tune=X['tune'], Y_tune=Y['tune'],
                                                X_merged=X['merged'], Y_merged=Y['merged'],
                                                X_test=X['test'], Y_test=Y['test'],
                                                np=50, goal=goal, life=10, cr=0.8, f=0.5)

            # Run the tuner
            tuned_test_score, best_params, tune_score, untuned_test_score = de_tuner.tune_and_evaluate(n_DE=1)

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


    # Dump the python dictionary to a file
    with open(results_base_dir+"%s_tune.py"%(dataset),"w+") as res_file:
        res_file.write(str(results))
    print(results)

    k_file.close()

