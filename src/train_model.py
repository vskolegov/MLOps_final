import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.datasets import load_wine
import pickle

def train_model(data=None):
    if data is None:
        wine = load_wine()
        data = pd.DataFrame(data=np.c_[wine['data'], wine['target']],
                            columns=wine['feature_names'] + ['target'])

    X_train = data.drop('target', axis=1)
    y_train = data['target']

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)

    with open('model.pkl', 'wb') as f:
        pickle.dump(clf, f)

if __name__ == "__main__":
    train_model()
