import pickle
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

app = FastAPI()

class WineFeatures(BaseModel):
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: float
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315_of_diluted_wines: float
    proline: float

# Load the model
def load_model():
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)
        return model, label_encoder
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

model, label_encoder = load_model()

@app.post("/predict")
def predict(features: WineFeatures):
    if not model or not label_encoder:
        return {"error": "Model not loaded"}
    data = pd.DataFrame([features.dict().values()], columns=features.dict().keys())
    prediction = model.predict(data)
    prediction_label = label_encoder.inverse_transform(prediction)
    return {"prediction": prediction_label[0]}

@app.post("/train")
async def train_model(file: UploadFile = File(...)):
    # Load dataset
    df = pd.read_csv(file.file)
    
    # Split dataset
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Train model
    clf = tree.DecisionTreeClassifier()
    clf.fit(X, y)
    
    # Train label encoder
    label_encoder = LabelEncoder()
    label_encoder.fit(y)
    
    # Save model
    with open('model.pkl', 'wb') as f:
        pickle.dump(clf, f)
    
    # Save label encoder
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    return {"status": "Model trained and saved"}

@app.post("/upload_model")
async def upload_model(file: UploadFile = File(...)):
    # Save uploaded model file
    with open('model.pkl', 'wb') as f:
        content = await file.read()
        f.write(content)
    return {"status": "Model uploaded successfully"}
