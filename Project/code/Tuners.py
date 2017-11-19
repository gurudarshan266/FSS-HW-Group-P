from DE import DiffentialEvolutionTuner
from preprocess import preprocess

import numpy as np
from sklearn.svm import SVC
from sklearn import tree
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

paramgrid_cart = {
             "max_features": np.linspace(start=0.1,stop=1.0,num=99),
             "max_depth": range(1,51),
             "min_samples_split": range(2,21),
             "min_samples_leaf": range(1,21)
             }

# Fetch training, tuning and testing datasets for lucene
X,Y = preprocess(dataset='lucene', do_smote = True)

de_tuner = DiffentialEvolutionTuner(learner=tree.DecisionTreeClassifier(), param_grid=paramgrid_cart,
                                    X_train=X['train'], Y_train=Y['train'],
                                    X_tune=X['tune'], Y_tune=Y['tune'],
                                    X_merged=X['merged'], Y_merged=Y['merged'],
                                    np=100, goal="f1", life=10, cr=0.3, f=0.6)

de_tuner.tune_and_evaluate(X['test'],Y['test'],5)

tr = tree.DecisionTreeClassifier()
tr.fit(X['merged'], Y['merged'])
Y_predict =  tr.predict(X['test'])
score = f1_score(Y['test'], Y_predict)
print("Untuned Score = %f"%score)