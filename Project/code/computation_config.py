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
            #"mlp",
            "knn"]

learner_objs = {"cart": tree.DecisionTreeClassifier(random_state=SEED_CART),
                "rf": RandomForestClassifier(random_state=SEED_RF),
                "nb": GaussianNB(),
                "svm": SVC(random_state=SEED_SVM),
                "mlp": MLPClassifier(random_state=SEED_MLP),
                "knn": KNeighborsClassifier()
                }

learner_objs2 = {"cart": tree.DecisionTreeClassifier(random_state=SEED_CART),
                "rf": RandomForestClassifier(random_state=SEED_RF),
                "nb": GaussianNB(),
                "svm": SVC(random_state=SEED_SVM),
                "mlp": MLPClassifier(random_state=SEED_MLP),
                "knn": KNeighborsClassifier()
                }

ensemble_weights = {}
ensemble_weights["f1"] = {
    "lucene": {"nb":1,"knn":2, "cart":2, "rf":3, "svm":4},
    "ivy": {"cart":1, "svm":1, "nb":2, "rf":2,"knn":2},
    "xalan1": {"svm":1, "nb":2, "cart":3, "knn":4, "rf":4},
    "xerces": {"cart":3, "rf":5, "nb":2, "svm":1, "knn":4}
}