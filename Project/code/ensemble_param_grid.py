import param_grid as pg
import computation_config as cc
import copy

def get_ensemble_params(learners, ensemble_name):
    result = {}
    for learner in learners:
        params = pg.param_grid[learner]
        for p in params:
            result['%s__%s'%(learner,p)] = copy.deepcopy(pg.param_grid[learner][p])
    print(result)
    pg.param_grid[ensemble_name] = result
    return result

if __name__ == '__main__':
    get_ensemble_params(cc.learners)