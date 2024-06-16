import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import dvc.api
import os
import pickle

def get_available_datasets():
    datasets = []
    with dvc.api.open('data/', repo='https://github.com/vskolegov/MLOps_final') as fd:
        for entry in os.listdir(fd):
            datasets.append(entry)
    return datasets

# Define function to train the model on a selected dataset
def train_model(dataset_name):
    dataset_path = f'data/{dataset_name}'
    data_url = dvc.api.get_url(path=dataset_path, repo='https://github.com/vskolegov/MLOps_final')
    
    data = pd.read_csv(data_url)
    X = data.drop('target', axis=1)
    y = data['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Model trained with accuracy: {accuracy}')
    
if __name__ == "__main__":
    available_datasets = get_available_datasets()
    print("Available datasets:", available_datasets)
    train_model('wine_data_full.csv')  # Example to train on the full dataset
