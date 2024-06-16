import dvc.api
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle

# Get data URL from DVC
data_url = dvc.api.get_url('data/wine_data_full.csv', repo='https://github.com/vskolegov/MLOps_final')

# Load data
data = pd.read_csv(data_url)

# Split data
X_train = data[:-20]
X_test = data[-20:]

y_train = X_train.target
y_test = X_test.target

X_train = X_train.drop('target', axis=1)
X_test = X_test.drop('target', axis=1)

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
print("accuracy_score: %.2f" % accuracy_score(y_test, y_pred))
