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


class DiffentialEvolutionTuner:
    "Hyperparameter tuning using Differential Evolution Tuned"
    def __init__(self, learner, param_grid = None,
                  X_train= None, Y_train = None,
                  X_tune=None, Y_tune=None,
                  X_test=None, Y_test=None,
                  X_merged=None, Y_merged=None,
                  cv=None, np = 50, f = 0.75, cr = 0.5, life = 10, goal = "accuracy"):

        random.seed(422)

        # Logger config
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize the learner and DE params
        self.learner = learner

        self.np = np
        self.f = f
        self.cr = cr
        self.life = life

        # TODO: Check if the goal is supported by the model
        self.goal = goal

        # Check that X_train and Y_train have correct shape
        if X_train is not None and Y_train is not None:
            self.X_train, self.Y_train = check_X_y(X_train, Y_train)

        self.cv_required = cv is not None

        # If no cross val object is provided, use tuned model
        if not self.cv_required:
            # Check that X_train and Y_train have correct shape
            if X_tune is not None and Y_tune is not None:
                self.X_tune, self.Y_tune = check_X_y(X_tune, Y_tune)
                self.X_merged, self.Y_merged = check_X_y(X_merged, Y_merged)
                self.X_test, self.Y_test = check_X_y(X_test, Y_test)

        else:
            self.cv = cv

        self.param_grid = param_grid

        # Compute bounds for all the numeric variable
        self.compute_bounds(self.param_grid)

        # Compute the score with untuned (default) learner
        self.computed_untuned_score()

    def validate_param_grid(self,param_grid):
        "Checks for any unsupported params"
        model_params = self.learner.get_params().keys()
        for k in param_grid:
            if k not in model_params:
                print("%s is not supported"%k)
                return False
        return True


    def compute_bounds(self, param_grid):
        model_params = self.learner.get_params().keys()
        self.bounds = {}
        for k in param_grid:
            # Only applicable for numeric fields
            if type(param_grid[k][0]) is float or type(param_grid[k][0]) is int:
                self.bounds[k] = {'max': max(param_grid[k]), 'min': min(param_grid[k])}


    def trim(self, param, val):
        "Trim the value to the bounds of the grid"
        if param in self.bounds:
            val = max(val,self.bounds[param]['min'])
            val = min(val,self.bounds[param]['max'])
        return val


    def generate_population(self, np):
        '''Generate the initial population'''

        population = []
        # random.seed()
        for i in range(np):
            member = ParamSet()
            # Create a member by randomly picking up param values from the grid
            for param in self.param_grid:
                member[param] = copy.deepcopy(random.choice(self.param_grid[param]))
            population.append(member)
        return population


    def n_tune_hyperparams(self, n_DE = 5):
        '''Execute DE for n iterations with different Generation 0'''
        best_params = None
        best_score = -float('inf')

        for i in range(n_DE):
            self.logger.debug("Executing Iteration #%d of DE"%(i+1))
            i_params, i_score = self.tune_hyperparams()
            if i_score > best_score:
                best_score = i_score
                best_params = i_params

        return (best_params,best_score)


    def tune_hyperparams(self):
        if not self.validate_param_grid(self.param_grid):
            raise ValueError

        # Create initial population
        population = self.generate_population(np=self.np)

        best_score = -float("inf")
        best_member = None

        for gen in range(1,self.life+1):
            print("\nRunning generation %d\n"%gen)
            #print(*population,sep='\n')

            new_generation = []
            for member in population:
                new_member = self.extrapolate(member, population, self.cr, self.f)

                new_mem_score = self.score(new_member)
                mem_score = self.score(member)

                # Check if the new member's score is better than the member's score
                if new_mem_score > mem_score:
                    new_generation.append(new_member)
                    self.logger.debug("New member added : %s" % str(new_member))

                    # Update the best score
                    if new_mem_score > best_score:
                        best_score = new_mem_score
                        best_member = new_member

                else:
                    new_generation.append(member)

                    # Update the best score
                    if mem_score > best_score:
                        best_score = mem_score
                        best_member = member

            # Update the population to new generation
            population = new_generation

            print( "Best member of population is %s with score = %f" % (str(best_member), float(best_score)) )

        return (best_member.params, best_score)


    def extrapolate(self, member, population, cr, f):
        population2 = [ m for m in population if m!=member]
        #random.seed()
        other3 = random.sample(population2,3)
        a, b, c = other3

        new_member = member.clone()
        changed = False

        for k in a.params:
            if random.random() <= cr:
                changed = True

                if type(member[k]) is float:
                    new_member[k] = a[k] + f*(b[k]-c[k])
                    new_member[k] = self.trim(k, new_member[k])

                elif type(member[k]) is int:
                    new_member[k] = int(a[k] + f * (b[k] - c[k]))
                    new_member[k] = self.trim(k, new_member[k])

                elif type(member[k]) is str or type(member[k]) is tuple:
                    # Randomly choose of from one of the population
                    x = random.randint(0, 2)
                    new_member[k] = other3[x][k]

        # If nothing has changed
        if not changed:
            k = random.choice(list(a.params.keys()))
            new_member[k] = b[k]

        return new_member


    def score(self, mem):
        #self.logger.debug('Computing score for %s'%str(params))
        #print('Computing score for %s'%str(params))

        # Check if the score was already computed
        if mem.score is not None:
            return mem.score

        params = mem.params

        # Update the learner params
        # TODO: Check if the learner can be replicated without using the same instance. For multi threading
        #learner = copy.deepcopy(self.learner)
        self.learner.set_params(**params)

        # Only for non-cv path
        if not self.cv_required:
            # Fit the training data
            self.learner.fit(self.X_train, self.Y_train)

            # Predict the new values
            Y_predict = self.learner.predict(self.X_tune)

            # Select the score based on the goal returned
            if self.goal == "accuracy":
                mem.score = accuracy_score(self.Y_tune, Y_predict)
            elif self.goal == "f1":
                mem.score = f1_score(self.Y_tune, Y_predict)
            elif self.goal == "precision":
                mem.score = precision_score(self.Y_tune, Y_predict)
            elif self.goal == "recall":
                mem.score = recall_score(self.Y_tune, Y_predict)
            elif self.goal == "auc" or self.goal == "roc_auc":
                mem.score = roc_auc_score(self.Y_tune, Y_predict)

        return mem.score


    def tune_and_evaluate(self, n_DE=5):
        # Get the best params
        best_params, tune_score = self.n_tune_hyperparams(n_DE)

        X_test, Y_test = self.X_test, self.Y_test

        # Calculate tuned score
        self.learner.set_params(**best_params)
        self.learner.fit(self.X_merged, self.Y_merged)
        Y_predict =  self.learner.predict(X_test)
        score = 0

        # Select the score based on the goal returned
        if self.goal == "accuracy":
            score = accuracy_score(Y_test, Y_predict)
        elif self.goal == "f1":
            score = f1_score(Y_test, Y_predict)
        elif self.goal == "precision":
            score = precision_score(Y_test, Y_predict)
        elif self.goal == "recall":
            score = recall_score(Y_test, Y_predict)
        elif self.goal == "auc" or self.goal == "roc_auc":
            score = roc_auc_score(Y_test, Y_predict)

        print("\n\nUntuned Score = %f" % self.untuned_test_score)
        print("Tuned Score = %f" % score)

        return (score, best_params, tune_score, self.untuned_test_score)

    def computed_untuned_score(self):
        'Calculate untuned score. Must be called before the tuning'

        self.learner.fit(self.X_merged, self.Y_merged)
        Y_predict = self.learner.predict(self.X_test)
        self.untuned_test_score = 0

        # Select the score based on the goal returned
        if self.goal == "accuracy":
            self.untuned_test_score = accuracy_score(self.Y_test, Y_predict)
        elif self.goal == "f1":
            self.untuned_test_score = f1_score(self.Y_test, Y_predict)
        elif self.goal == "precision":
            self.untuned_test_score = precision_score(self.Y_test, Y_predict)
        elif self.goal == "recall":
            self.untuned_test_score = recall_score(self.Y_test, Y_predict)
        elif self.goal == "auc" or self.goal == "roc_auc":
            self.untuned_test_score = roc_auc_score(self.Y_test, Y_predict)
        return self.untuned_test_score







if __name__=='__main__':
    paramgrid = pg.param_grid['cart']
    learner = tree.DecisionTreeClassifier(random_state=1542)
    dataset = 'lucene'

    # Fetch training, tuning and testing datasets for lucene
    X,Y = preprocess(dataset=dataset, do_smote = True)

    de_tuner = DiffentialEvolutionTuner(learner=learner,param_grid=paramgrid,
                                        X_train=X['train'], Y_train=Y['train'],
                                        X_tune=X['tune'], Y_tune=Y['tune'],
                                        X_merged=X['merged'], Y_merged=Y['merged'],
                                        X_test=X['test'], Y_test=Y['test'],
                                        np=50, goal="f1", life=10, cr=0.8, f=0.5)

    de_tuner.tune_and_evaluate(1)



