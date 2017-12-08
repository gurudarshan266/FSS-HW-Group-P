import param_grid as pg
import computation_config as cc
import copy
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from DE import DiffentialEvolutionTuner
from preprocess import preprocess

def get_ensemble_params(learners, ensemble_name):
    result = {}
    for learner in learners:
        params = pg.param_grid[learner]
        for p in params:
            result['%s__%s'%(learner,p)] = copy.deepcopy(pg.param_grid[learner][p])
    #print(result)
    pg.param_grid[ensemble_name] = result
    return result

def ensemble_tune(goal='f1',dataset='lucene',sk_ranks=None):
    ensemble_estimators = []
    ensemble_weights = []
    sk_ranks = sk_ranks or cc.ensemble_weights[goal][dataset]

    # add the learners to the ensemble
    for learner in cc.learners:
        # Append ensemble learners and their correspondig weights based on the results from Scott-Knott test
        ensemble_estimators.append( (learner,cc.learner_objs2[learner],) )
        weight = sk_ranks[learner]
        ensemble_weights.append(weight)


    # print(ensemble_weights)
    # print(*ensemble_estimators,sep="\n")

    paramgrid = get_ensemble_params(cc.learners, ensemble_name="ensemble1")
    paramgrid['estimators'] = [ensemble_estimators]
    paramgrid['weights'] = [ensemble_weights]
    paramgrid['n_jobs'] = [-1]

    # create the ensemble learner
    eclf = VotingClassifier(estimators=ensemble_estimators,
                            weights=ensemble_weights,
                            n_jobs=-1
                            )

    # Fetch training, tuning and testing datasets for the dataset
    X, Y = preprocess(dataset=dataset, do_smote=True)

    # eclf = eclf.fit(X['train'], Y['train'])
    # print(eclf.predict(X['test']))

    # Instantiate the tuner
    de_tuner = DiffentialEvolutionTuner(learner=eclf, param_grid=paramgrid,
                                        X_train=X['train'], Y_train=Y['train'],
                                        X_tune=X['tune'], Y_tune=Y['tune'],
                                        X_merged=X['merged'], Y_merged=Y['merged'],
                                        X_test=X['test'], Y_test=Y['test'],
                                        np=100, goal=goal, life=10, cr=0.8, f=0.5)

    # Run the tuner
    tuned_test_score, best_params, tune_score, untuned_test_score = de_tuner.tune_and_evaluate(n_DE=1)

    return (tuned_test_score, best_params, tune_score, untuned_test_score)


if __name__ == '__main__':
    goal = 'f1'
    dataset = 'lucene'
    ensemble_tune(goal=goal, dataset=dataset)