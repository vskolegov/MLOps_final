from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
import os
from train_model import train_model

app = FastAPI()

def load_model():
    if os.path.exists('model.pkl'):
        with open('model.pkl', 'rb') as f:
            return pickle.load(f)
    return None

model = load_model()

class PredictionRequest(BaseModel):
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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict")
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=400, detail="Model is not trained yet.")
    data = np.array([[
        request.alcohol, request.malic_acid, request.ash, request.alcalinity_of_ash,
        request.magnesium, request.total_phenols, request.flavanoids, request.nonflavanoid_phenols,
        request.proanthocyanins, request.color_intensity, request.hue,
        request.od280_od315_of_diluted_wines, request.proline
    ]])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}

@app.post("/retrain")
def retrain(file: UploadFile = File(...)):
    with open("new_data.csv", "wb") as f:
        f.write(file.file.read())

    new_data = pd.read_csv("new_data.csv")
    train_model(new_data)

    global model
    model = load_model()

    return {"detail": "Model retrained successfully"}
