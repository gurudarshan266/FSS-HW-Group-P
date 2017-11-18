from DE import DiffentialEvolutionTuner
from preprocess import preprocess

import numpy as np
from sklearn.svm import SVC
from sklearn import tree

paramgrid_cart = {
             "max_features": np.linspace(start=0.0,stop=1.0,num=100),
             "max_depth": range(1,51),
             "min_samples_split": range(2,21),
             "min_samples_leaf": range(1,21)
             }

# Fetch training, tuning and testing datasets for lucene
X_train, Y_train, X_tune, Y_tune, X_test, Y_test, X_merged, Y_merged = preprocess(dataset='lucene', do_smote = True)

de_tuner = DiffentialEvolutionTuner(learner=tree.DecisionTreeClassifier(), param_grid=paramgrid_cart,
                                    X_train=X_train, Y_train=Y_train,
                                    X_tune=X_tune, Y_tune=Y_tune,
                                    X_merged=X_merged, Y_merged=Y_merged,
                                    np=40, goal="f1", life=20, cr=0.85, f=0.6)

de_tuner.tune_and_evaluate(X_test,Y_test,5)
