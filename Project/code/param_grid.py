import numpy as np

param_grid = {}

# CART
param_grid['cart'] = {
    "max_features": np.linspace(start=0.1, stop=1.0, num=99),
    "max_depth": range(1, 51),
    "min_samples_split": range(2, 21),
    "min_samples_leaf": range(1, 21),
    "random_state": [1542]
}

# Random Forests
param_grid['rf'] = {
    "max_features": np.linspace(start=0.1, stop=1.0, num=99),
    "max_leaf_nodes": range(1, 51),
    "min_samples_split": range(2, 21),
    "min_samples_leaf": range(1, 21),
    "n_estimators": range(50, 151),
}

# Naive Bayes
param_grid['nb'] = {
    "priors":  {None}
}

# Support Vector Machine
param_grid['svm'] = {
    "kernel": ["rbf", "sigmoid"],
    "C": np.logspace(-9, 9, num=10, base=10),
}

# Artificial Neural Nets (Multi Layer Perceptron Classifier)
param_grid['ann'] = {
    "hidden_layer_sizes": [(100,), (100,100,), (100,100,100,100,), (100,100,100,100,100,)],
    "activation": ['identity', 'logistic', 'tanh', 'relu'],
    "max_iter": range(100,400,50)

}


