from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # para permitir peticiones desde React

# Cargar modelo entrenado
model = joblib.load("src/model_pipeline.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Convertir a DataFrame
    df = pd.DataFrame([data])

    # Hacer predicción
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]  # probabilidad de que sea 1

    return jsonify({
        "prediction": int(prediction),
        "probability": round(float(probability), 3)
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
