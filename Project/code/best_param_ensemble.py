import param_grid as pg
import computation_config as cc
import copy
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from DE import DiffentialEvolutionTuner
from preprocess import preprocess
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

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

def get_ensemble_params(learners, ensemble_name):
    result = {}
    for learner in learners:
        params = pg.param_grid[learner]
        for p in params:
            result['%s__%s'%(learner,p)] = copy.deepcopy(pg.param_grid[learner][p])
    #print(result)
    pg.param_grid[ensemble_name] = result
    return result


def tune_best_param_ensembles(goal='f1',dataset='lucene',best_params=None, sk_ranks=None):
    ensemble_estimators = []
    ensemble_weights = []
    sk_ranks = sk_ranks or cc.ensemble_weights[goal][dataset]

    # best_params = {'xerces': {'cart': (
    # {'max_features': 0.10000000000000001, 'min_samples_split': 7, 'max_depth': 1, 'random_state': 1542,
    #  'min_samples_leaf': 13}, 0.3102803738317757, 0.69650349650349652),
    #             'nb': ({'priors': None}, 0.31238095238095243, 0.31238095238095243),
    #             'svm': ({'kernel': 'sigmoid', 'C': 1000000000.0}, 0.60606060606060619, 0.47389558232931722), 'rf': (
    #     {'max_features': 0.96326530612244898, 'min_samples_split': 17, 'max_leaf_nodes': 2, 'min_samples_leaf': 6,
    #      'n_estimators': 60}, 0.32293577981651378, 0.58024691358024683),
    #             'knn': ({'weights': 'uniform', 'n_neighbors': 3}, 0.5318818040435459, 0.46003262642740622)}}
    #
    # best_params['ivy'] = {'knn': ({'weights': 'uniform', 'n_neighbors': 8}, 0.23529411764705882, 0.23749999999999996),
    #                       'svm': ({'kernel': 'rbf', 'C': 10.0}, 0.034482758620689662, 0.035087719298245612),
    #                       'nb': ({'priors': None}, 0.3529411764705882, 0.3529411764705882), 'cart': (
    #     {'min_samples_split': 8, 'min_samples_leaf': 2, 'random_state': 1542, 'max_features': 0.9816326530612246,
    #      'max_depth': 15}, 0.31192660550458717, 0.2857142857142857), 'rf': (
    #     {'min_samples_split': 14, 'n_estimators': 108, 'max_leaf_nodes': 7, 'max_features': 0.86224489795918369,
    #      'min_samples_leaf': 1}, 0.27083333333333337, 0.32142857142857145)}
    #
    # best_params['lucene'] = {
    #     'svm': ({'C': 1.0000000000000001e-09, 'kernel': 'rbf'}, 0.6995708154506437, 0.73228346456692917),
    #     'nb': ({'priors': None}, 0.5298013245033113, 0.5298013245033113),
    #     'knn': ({'weights': 'uniform', 'n_neighbors': 5}, 0.63535911602209938, 0.63535911602209938), 'cart': (
    #     {'random_state': 1542, 'max_depth': 16, 'min_samples_leaf': 6, 'max_features': 0.10918367346938776,
    #      'min_samples_split': 6}, 0.60526315789473684, 0.66666666666666674), 'rf': (
    #     {'n_estimators': 50, 'min_samples_leaf': 16, 'max_features': 0.10000000000000001, 'min_samples_split': 11,
    #      'max_leaf_nodes': 7}, 0.64810126582278482, 0.65909090909090906)}


    # add the learners to the ensemble
    for learner in cc.learners:
        # Append ensemble learners and their correspondig weights based on the results from Scott-Knott test
        cc.learner_objs[learner].set_params(**best_params[dataset][learner][0])
        ensemble_estimators.append( (learner,cc.learner_objs[learner],) )
        weight = sk_ranks[learner]
        ensemble_weights.append(weight)


    # create the ensemble learner
    eclf = VotingClassifier(estimators=ensemble_estimators,
                            weights=ensemble_weights,
                            # n_jobs=-1
                            )

    # Fetch training, tuning and testing datasets for the dataset
    X, Y = preprocess(dataset=dataset, do_smote=True)

    eclf = eclf.fit(X['merged'], Y['merged'])
    Y_predict = eclf.predict(X['test'])

    return compute_score(goal=goal,Y_predict=Y_predict,Y_test=Y['test'])


if __name__ == '__main__':
    pass


