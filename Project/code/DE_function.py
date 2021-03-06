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
import logging
import copy
import matplotlib.pyplot as plt
from ParamSet import ParamSet


class DiffentialEvolutionTuner:
    "Hyperparameter tuning using Differential Evolution Tuned"
    def __init__(self, learner, param_grid = None,
                  X_train= None, Y_train = None,
                  X_tune=None, Y_tune=None,
                  cv=None, np = 50, f = 0.75, cr = 0.5, life = 10, goal = "accuracy"):

        random.seed()

        # Logger config
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        #Initialize the learner and DE params
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
        else:
            self.cv = cv

        self.param_grid = param_grid

        # Compute bounds for all the numeric variable
        self.compute_bounds(self.param_grid)


    def validate_param_grid(self,param_grid):
        "Checks for any unsupported params"
        model_params = self.learner.get_params().keys()
        for k in param_grid:
            if k not in model_params:
                return False
        return True


    def compute_bounds(self, param_grid):
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
        for i in range(np):
            member = ParamSet()
            random.seed()
            # Create a member by randomly picking up param values from the grid
            for param in self.param_grid:
                member[param] = copy.deepcopy(random.choice(self.param_grid[param]))
            population.append(member)

        print(*population,sep='\n')
        return population


    def tune_hyperparams(self):
        # if not self.validate_param_grid(self.param_grid):
        #     raise ValueError

        # Create initial population
        population = self.generate_population(np=self.np)

        best_score = -float("inf")
        best_member = None

        for gen in range(1,self.life+1):
            print("\nRunning generation %d\n"%gen)
            self.plot_population(population,gen)
            #print(*population,sep='\n')

            new_generation = []
            for member in population:
                new_member = self.extrapolate(member, population, self.cr, self.f)

                new_mem_score = self.score_func(new_member)
                mem_score = self.score_func(member)

                # Check if the new member's score is better than the member's score
                if new_mem_score > mem_score:
                    new_generation.append(new_member)
                    print("New member added : %s"%str(new_member))

                    # Update the best score
                    if new_mem_score > best_score:
                        best_score = new_mem_score
                        best_member = new_member

                else:
                    new_generation.append(member)
                    print("Existing member added : %s" % str(new_member))

                    # Update the best score
                    if mem_score > best_score:
                        best_score = mem_score
                        best_member = member

            # Update the population to new generation
            population = new_generation

            print( "Best member of population is %s with score = %f" % (str(best_member), float(best_score)) )

        return (best_member, best_score)


    def extrapolate(self, member, population, cr, f):
        population2 = [ m for m in population if m!=member]
        #random.seed(random.randint(1,50))
        other3 = random.sample(population2,3)
        a, b, c = other3

        new_member = member.clone()
        changed = False

        for k in a.params:
            if random.uniform(0,1.0) <= cr:
                changed = True

                if type(member[k]) is float:
                    new_member[k] = a[k] + f*(b[k]-c[k])
                    new_member[k] = self.trim(k, new_member[k])

                elif type(member[k]) is int:
                    new_member[k] = int(a[k] + f * (b[k] - c[k]))
                    new_member[k] = self.trim(k, new_member[k])

                elif type(member[k]) is str:
                    # Randomly choose of from one of the population
                    x = random.randint(0, 2)
                    new_member[k] = other3[x][k]

        # If nothing has changed
        if not changed:
            k = random.choice(list(a.params.keys()))
            new_member[k] = b[k]

        return new_member


    def score(self, params):
        #self.logger.debug('Computing score for %s'%str(params))
        #print('Computing score for %s'%str(params))

        # Update the learner params
        # TODO: Check if the learner can be replicated without using the same instance. For multi threading
        self.learner.set_params(**params)

        # Only for non-cv path
        if not self.cv_required:
            # Fit the training data
            self.learner.fit(self.X_train, self.Y_train)

            # Predict the new values
            Y_predict = self.learner.predict(self.X_tune)

            # Select the score based on the goal returned
            if self.goal == "accuracy":
                return accuracy_score(self.Y_tune, Y_predict)
            elif self.goal == "f1":
                return f1_score(self.Y_tune, Y_predict)
            elif self.goal == "precision":
                return precision_score(self.Y_tune, Y_predict)
            elif self.goal == "recall":
                return recall_score(self.Y_tune, Y_predict)
            elif self.goal == "auc" or self.goal == "roc_auc":
                return roc_auc_score(self.Y_tune, Y_predict)


    def score_func(self, mem):
        #self.logger.debug('Computing score for %s'%str(params))
        # print('Computing score for %s'%str(params))
        if mem.score is None:
            mem.score = self.learner(**mem.params)
        return mem.score

    def plot_population(self, population, gen):
        return
        X = [ mem['x'] for mem in population]
        Y = [ mem['y'] for mem in population]
        #fig = plt.figure(gen)
        plt.scatter(X, Y, s=20*20.0, alpha=0.5)
        plt.title('Genearation %d'%gen )
        plt.xlabel('x')
        plt.ylabel('y')
       # plt.ion()
        plt.show()

    def random_pick(self, arr):
        n = random.uniform(0,len(arr)+0.1)
        return arr[int(n)]

if __name__=='__main__':
    paramgrid = {"kernel": ["rbf","sigmoid"],
                 "C": np.logspace(-9, 9, num=10, base=10),
                 #"C": np.linspace(start=1,stop=100000,num=13),
                 #"gamma": np.logspace(-9, 9, num=10, base=10)
                 }

    paramgrid = {"x" : np.linspace(start=-10,stop=10, num=1000),
                 "y": np.linspace(start=-10, stop=10, num=1000)}

    f = lambda x,y: 5-x**2-y**2

    # Fetch training, tuning and testing datasets for lucene
    X_train, Y_train, X_tune, Y_tune, X_test, Y_test = preprocess(dataset='lucene', do_smote = True)

    de_tuner = DiffentialEvolutionTuner(learner=f,param_grid=paramgrid,
                                        X_train=X_train, Y_train=Y_train,
                                        X_tune=X_tune, Y_tune=Y_tune,
                                        np=40, goal="f1",life=40, f=0.6, cr=0.9)
    best_params, best_score = de_tuner.tune_hyperparams()


