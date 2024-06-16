import os
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import subprocess
import threading

app = FastAPI()

class PredictionRequest(BaseModel):
    Alcohol: float = 14.2
    Malic_acid: float = 1.71
    Ash: float = 2.43
    Alcalinity_of_ash: float = 15.6
    Magnesium: float = 127
    Total_phenols: float = 2.8
    Flavanoids: float = 3.06
    Nonflavanoid_phenols: float = 0.28
    Proanthocyanins: float = 2.29
    Color_intensity: float = 5.64
    Hue: float = 1.04
    OD280_OD315_of_diluted_wines: float = 3.92
    Proline: float = 1065

def load_model():
    global model, label_encoder
    model_path = 'model.pkl'
    label_encoder_path = 'label_encoder.pkl'
    
    if os.path.exists(model_path) and os.path.exists(label_encoder_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(label_encoder_path, 'rb') as f:
            label_encoder = pickle.load(f)
    else:
        raise FileNotFoundError("Model or Label Encoder not found")

@app.on_event("startup")
async def startup_event():
    load_model()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/predict/")
async def predict(request: PredictionRequest):
    try:
        data = pd.DataFrame([request.dict()])
        data.columns = [
            'Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash', 'Magnesium', 'Total phenols', 
            'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins', 'Color intensity', 'Hue', 
            'OD280/OD315 of diluted wines', 'Proline'
        ]
        predictions = model.predict(data)
        predictions = label_encoder.inverse_transform(predictions)
        return JSONResponse(content={"predictions": predictions.tolist()})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/labels/")
async def get_labels():
    try:
        labels = label_encoder.classes_.tolist()
        return JSONResponse(content={"labels": labels})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/retrain/")
async def retrain():
    def retrain_model():
        try:
            # Pull the latest data
            result = subprocess.run(['dvc', 'pull'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error pulling data: {result.stderr}")
                return {"status": "failed", "detail": result.stderr}
            
            # Retrain the model
            result = subprocess.run(['python', 'src/train_model.py'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error training model: {result.stderr}")
                return {"status": "failed", "detail": result.stderr}
            
            # Reload the model after retraining
            load_model()
            return {"status": "success"}
        except Exception as e:
            print(f"Exception during retraining: {e}")
            return {"status": "failed", "detail": str(e)}
    
    threading.Thread(target=retrain_model).start()
    return JSONResponse(content={"status": "started", "detail": "Retraining has been started. Please check back later."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
