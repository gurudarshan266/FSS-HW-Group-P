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


if __name__=='__main__':

    dataset = 'lucene'
    results = {}
    header = "Learner|Best Params|Untuned Score|Tuned Score"

    with open("results/%s_results.csv"%dataset, "w+") as file:
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
                                                np=50, goal="f1", life=10, cr=0.8, f=0.5)

            # Run the tuner
            tuned_test_score, best_params, tune_score, untuned_test_score = de_tuner.tune_and_evaluate(n_DE=1)

            results[dataset][learner] = (best_params, untuned_test_score, tuned_test_score)

            file.write("%s|%s|%f|%f\n"%(learner,best_params, untuned_test_score, tuned_test_score))
            file.flush()

    print(results)

