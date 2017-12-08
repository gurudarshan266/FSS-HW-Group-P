from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.svm import SVC
from preprocess import preprocess

X,Y = preprocess(dataset='lucene', do_smote = True)

sv1 = SVC(kernel='rbf')
sv1.fit(X['train'],Y['train'])
Y_predict = sv1.predict(X['test'])
print("F1 score = %f"%f1_score(Y['test'],Y_predict))

sv1.set_params(kernel="sigmoid")
sv1.fit(X['train'],Y['train'])
Y_predict = sv1.predict(X['test'])
print("F1 score = %f"%f1_score(Y['test'],Y_predict))


sv2 = SVC(kernel='sigmoid')
sv2.fit(X['train'],Y['train'])
Y_predict = sv2.predict(X['test'])
print("F1 score = %f"%f1_score(Y['test'],Y_predict))

sv2.set_params(kernel="rbf")
sv2.fit(X['train'],Y['train'])
Y_predict = sv2.predict(X['test'])
print("F1 score = %f"%f1_score(Y['test'],Y_predict))