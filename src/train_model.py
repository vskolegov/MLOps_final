import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle
import dvc.api

def load_data_from_dvc(file_path):
    with dvc.api.open(file_path, remote='myremote') as fd:
        return pd.read_csv(fd)

def get_available_datasets():
    datasets = dvc.api.ls(remote='myremote', path='data')
    dataset_names = [os.path.basename(dataset) for dataset in datasets]
    return dataset_names

def train_model(dataset_name):
    # Load data
    data = load_data_from_dvc(f'data/{dataset_name}')

    # Split data
    X = data.drop('target', axis=1)
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Train model
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)

    # Train label encoder
    label_encoder = LabelEncoder()
    label_encoder.fit(y_train)

    # Save model
    with open('model.pkl', 'wb') as f:
        pickle.dump(clf, f)

    # Save label encoder
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)

    # Predict and evaluate
    y_pred = clf.predict(X_test)
    print(f"accuracy_score for dataset {dataset_name}: %.2f" % accuracy_score(y_test, y_pred))

# Example usage:
if __name__ == "__main__":
    available_datasets = get_available_datasets()
    print("Available datasets:", available_datasets)
    selected_dataset = available_datasets[0]  # or choose another method to select dataset
    train_model(selected_dataset)
