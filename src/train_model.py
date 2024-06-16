import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle

def train_and_save_model():
    data = pd.read_csv('data/wine_data_full.csv')

    data.rename(columns={'Class': 'target'}, inplace=True)

    X = data.drop(columns=["target"])
    y = data["target"]

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)

    label_encoder = LabelEncoder()
    label_encoder.fit(y)

    with open('model.pkl', 'wb') as f:
        pickle.dump(clf, f)

    # Save label encoder
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)

    print("Model and label encoder saved successfully")

if __name__ == "__main__":
    train_and_save_model()
