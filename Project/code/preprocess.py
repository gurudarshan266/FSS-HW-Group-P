import pandas as pd
from imblearn.over_sampling import SMOTE

def preprocess(dataset='lucene', do_smote = True):
    bug_classify = lambda x: 1 if x > 0 else 0

    if dataset == 'lucene':
        file_train = 'lucene-2.0.csv'
        data_train = pd.read_csv(file_train)

        file_tune = 'lucene-2.2.csv'
        data_tune = pd.read_csv(file_tune)

        file_test = 'lucene-2.4.csv'
        data_test = pd.read_csv(file_test)

        # For extracting based on column name
        X_train = data_train.loc[:, 'wmc':'avg_cc']
        X_tune = data_tune.loc[:, 'wmc':'avg_cc']
        X_test = data_test.loc[:, 'wmc':'avg_cc']

        # For extracting based on column name
        Y_train = data_train.bug
        Y_tune = data_tune.bug
        Y_test = data_test.bug

        # Classify bugs as only binary (0 or 1)
        Y_train = Y_train.apply(bug_classify)
        Y_tune = Y_tune.apply(bug_classify)
        Y_test = Y_test.apply(bug_classify)

        # SMOTE the training data
        if do_smote:
            sm = SMOTE(random_state=42)
            X_train, Y_train = sm.fit_sample(X_train, Y_train)

        return (X_train,Y_train,X_tune,Y_tune,X_test, Y_test)