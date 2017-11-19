from DE import DiffentialEvolutionTuner
from preprocess import preprocess
from defines import *

from sklearn.svm import SVC
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

# Datasets examined
datasets = ["ivy",
            "jedit1",
            "jedit2",
            "jedit3",
            "lucene",
            "velocity",
            "xalan1",
            "xalan2",
            "xerces"]

learners = ["cart",
            "rf",
            "nb",
            "svm",
            "mlp",
            "knn"]

learner_objs = {"cart": tree.DecisionTreeClassifier(random_state=SEED_CART),
                "rf": RandomForestClassifier(random_state=SEED_RF),
                "nb": GaussianNB(),
                "svm": SVC(random_state=SEED_SVM),
                "mlp": MLPClassifier(random_state=SEED_MLP),
                "knn": KNeighborsClassifier()
                }

