from DE import DiffentialEvolutionTuner
import sklearn.datasets
import numpy as np
import random
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from preprocess import preprocess

from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from mlxtend.classifier import StackingClassifier
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold

clf1 = KNeighborsClassifier(n_neighbors=1)
clf2 = RandomForestClassifier(random_state=1)
clf3 = GaussianNB()
clf4 = SVC()
lr = LogisticRegression()
sclf = StackingClassifier(classifiers=[ clf1, clf2, clf3],
                          meta_classifier=lr)

params = {'kneighborsclassifier__n_neighbors': [1,2,3,4,5,6,8],
          'randomforestclassifier__n_estimators': [10,15,20,25,30,40, 50],
          #'svc__C':list(np.logspace(-9, 9, num=25, base=10)),
          'meta-logisticregression__C': [0.1, 10.0]}

random.seed(1)

# Fetch training, tuning and testing datasets for lucene
X_train, Y_train, X_tune, Y_tune, X_test, Y_test = preprocess(dataset='lucene', do_smote=True)

de_tuner = DiffentialEvolutionTuner(learner=sclf, param_grid=params,
                                    X_train=X_train, Y_train=Y_train,
                                    X_tune=X_tune, Y_tune=Y_tune,
                                    np=100, goal="accuracy")
best_params, best_score = de_tuner.tune_hyperparams()

sclf.fit(X_train, Y_train)
Y_predict = sclf.predict(X_test)
acc = accuracy_score(Y_test, Y_predict)
print("\n\nAccuracy = %f" % acc)

