import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import dvc.api
import os

app = FastAPI()

def get_available_datasets():
    datasets = dvc.api.ls(remote='myremote', path='data')
    dataset_names = [os.path.basename(dataset) for dataset in datasets]
    return dataset_names

def load_model_and_encoder():
    model_path = 'model.pkl'
    encoder_path = 'label_encoder.pkl'

    if os.path.exists(model_path) and os.path.exists(encoder_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(encoder_path, 'rb') as f:
            label_encoder = pickle.load(f)
        return model, label_encoder
    else:
        raise HTTPException(status_code=404, detail="Model or label encoder not found")

def train_model(dataset_name):
    # Implementation of training as in train_model.py
    ...

class PredictionRequest(BaseModel):
    data: dict

class TrainRequest(BaseModel):
    dataset_name: str

@app.get("/datasets")
async def list_datasets():
    return get_available_datasets()

@app.post("/predict")
async def predict(request: PredictionRequest):
    input_data = pd.DataFrame([request.data])

    model, label_encoder = load_model_and_encoder()

    predictions = model.predict(input_data)
    decoded_predictions = label_encoder.inverse_transform(predictions)
    return {"predictions": decoded_predictions.tolist()}

@app.post("/train")
async def train(request: TrainRequest):
    dataset_name = request.dataset_name
    if dataset_name not in get_available_datasets():
        raise HTTPException(status_code=404, detail="Dataset not found")
    train_model(dataset_name)
    return {"detail": f"Model trained on dataset {dataset_name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
