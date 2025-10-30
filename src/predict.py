import argparse
import pandas as pd
import joblib

def main():
    parser = argparse.ArgumentParser(description="Hacer predicciones con el modelo entrenado")
    parser.add_argument("input_csv", type=str, help="Ruta del archivo CSV con los nuevos datos")
    parser.add_argument("--model", type=str, default="src/model_pipeline.pkl", help="Ruta del modelo entrenado (.pkl)")
    parser.add_argument("--out", type=str, default="predicciones.csv", help="Ruta de salida para guardar las predicciones")
    args = parser.parse_args()

    # 1️⃣ Cargar los datos nuevos
    print("📂 Cargando datos desde:", args.input_csv)
    data = pd.read_csv(args.input_csv)

    # 2️⃣ Cargar el modelo
    print("🧠 Cargando modelo desde:", args.model)
    model = joblib.load(args.model)

    # 3️⃣ Hacer las predicciones
    print("🔮 Realizando predicciones...")
    predictions = model.predict(data)

    # 4️⃣ Agregar las predicciones al DataFrame
    data["prediccion_deposit"] = predictions

    # 5️⃣ Guardar los resultados
    data.to_csv(args.out, index=False)
    print(f"✅ Predicciones guardadas en: {args.out}")

if __name__ == "__main__":
    main()
