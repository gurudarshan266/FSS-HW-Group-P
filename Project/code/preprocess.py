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

    # Map the datasets to training, tuning and testing datasets
    filename = {}

    filename['ivy'] = {'train':'ivy-1.1.csv', 'tune':'ivy-1.4.csv', 'test':'ivy-2.0.csv'}

    filename['jedit1'] = {'train': 'jedit-3.2.csv', 'tune': 'jedit-4.0.csv', 'test': 'jedit-4.1.csv'}
    filename['jedit2'] = {'train': 'jedit-4.0.csv', 'tune': 'jedit-4.1.csv', 'test': 'jedit-4.2.csv'}
    filename['jedit3'] = {'train': 'jedit-4.1.csv', 'tune': 'jedit-4.2.csv', 'test': 'jedit-4.3.csv'}

    filename['lucene'] = {'train':'lucene-2.0.csv', 'tune':'lucene-2.2.csv', 'test':'lucene-2.4.csv'}

    filename['velocity'] = {'train': 'velocity-1.4.csv', 'tune': 'velocity-1.5.csv', 'test': 'velocity-1.6.csv'}

    filename['xalan1'] = {'train': 'xalan-2.4.csv', 'tune': 'xalan-2.5.csv', 'test': 'xalan-2.6.csv'}
    filename['xalan2'] = {'train': 'xalan-2.5.csv', 'tune': 'xalan-2.6.csv', 'test': 'xalan-2.7.csv'}

    filename['xerces'] = {'train':'xerces-1.2.csv', 'tune':'xerces-1.3.csv', 'test':'xerces-1.4.csv'}


    # Add base dirs for the file names
    file = { 'train':base_dir+filename[dataset]['train'], 'tune':base_dir+filename[dataset]['tune'], 'test':base_dir+filename[dataset]['test']}
    for t in dataset_types:
        data[t] = pd.read_csv(file[t])

        # Extract features
        X[t] = data[t].loc[:, 'wmc':'avg_cc']

        # Extract bugs and classify bugs as only binary (0 or 1)
        Y[t] = data[t].bug.apply(bug_classify)

    data['merged'] = pd.concat( [data['train'],data['tune']] )
    X['merged'] = data['merged'].loc[:, 'wmc':'avg_cc']
    Y['merged'] = data['merged'].bug.apply(bug_classify)

    # SMOTE the training data
    if do_smote:
        sm = SMOTE(random_state=1547)
        X['train'], Y['train'] = sm.fit_sample(X['train'], Y['train'])
        X['merged'], Y['merged'] = sm.fit_sample(X['merged'], Y['merged'])

    return (X,Y)

if __name__ == '__main__':
    pass