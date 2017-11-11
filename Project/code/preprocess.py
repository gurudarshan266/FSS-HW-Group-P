import pandas as pd
import sys
from imblearn.over_sampling import SMOTE


def preprocess(dataset='lucene', do_smote = True):
    bug_classify = lambda x: 1 if x > 0 else 0
    base_dir = "../datasets/"

    dataset_types = {'train','tune','test'}
    data = {}
    X = {}
    Y = {}
    if dataset == 'lucene':
        file = { 'train':base_dir+'lucene-2.0.csv', 'tune':base_dir+'lucene-2.2.csv', 'test':base_dir+'lucene-2.4.csv'}
        for t in dataset_types:
            data[t] = pd.read_csv(file[t])

            # Extract features
            X[t] = data[t].loc[:, 'wmc':'avg_cc']

            # Extract bugs and classify bugs as only binary (0 or 1)
            Y[t] = data[t].bug.apply(bug_classify)

        # SMOTE the training data
        if do_smote:
            sm = SMOTE(random_state=1516)
            X['train'], Y['train'] = sm.fit_sample(X['train'], Y['train'])

        return (X['train'],Y['train'],
                X['tune'],Y['tune'],
                X['test'], Y['test'])