# src/api/main.py
from fastapi import FastAPI, HTTPException
from datetime import datetime
from sqlalchemy import create_engine, text
import joblib
import pandas as pd
import os
import json

from src.api.schemas import InputRecord

MODEL_PATH = os.getenv("MODEL_PATH", "/app/model_pipeline.pkl")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/predictions")

app = FastAPI(title="Banking Campaign Predictor")

@app.on_event("startup")
def startup():
    global model, engine
    model = joblib.load(MODEL_PATH)
    engine = create_engine(DATABASE_URL)

@app.post("/predict")
def predict(record: InputRecord):
    df = pd.DataFrame([record.dict()])
    try:
        proba = float(model.predict_proba(df)[:,1][0])
        pred = int(model.predict(df)[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al predecir: {e}")

    # Guardar en BD
    query = text("""
        INSERT INTO predictions (input_json, predicted, probability, created_at)
        VALUES (:input_json, :predicted, :probability, :created_at)
    """)
    engine.execute(query, {
        "input_json": json.dumps(record.dict(), default=str),
        "predicted": pred,
        "probability": proba,
        "created_at": datetime.utcnow()
    })

    return {"predicted": pred, "probability": proba}
