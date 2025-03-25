from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib

# Crear la aplicación Flask
app = Flask(__name__)

# Cargar el modelo guardado
model = load_model("modelo_precio.keras")

# Suponiendo que el escalador se usó antes en el preprocesamiento
scaler_entrada = MinMaxScaler()
scaler = joblib.load("scaler_price.pkl")

def procesar_entrada(df):
    df["bedrooms_per_story"] = df["bedrooms"] / df["stories"]
    df["bathrooms_per_story"] = df["bathrooms"] / df["stories"]
    df["total_rooms"] = df["bedrooms"] + df["bathrooms"]
    df["stories_per_area"] = df["stories"] / df["area"]
    df["parking_per_area"] = df["parking"] / df["area"]
    df["stories_area_interaction"] = df["stories"] * df["area"]

    return df


# curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"area\": 8000, \"bedrooms\": 3, \"bathrooms\": 2, \"stories\": 2, \"mainroad\": 1, \"guestroom\": 0, \"basement\": 0, \"hotwaterheating\": 0, \"airconditioning\": 1, \"parking\": 2, \"prefarea\": 1, \"furnishingstatus\": 2}"
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Recibir los datos en formato JSON
        data = request.get_json()

        if not data:
            no_data = {"460": "No data sent"}
            return jsonify(no_data), 460

        if not isinstance(data, dict):
            incor_format = {"415": "Incorrect data format"}
            return jsonify(incor_format), 415

        # Convertir a DataFrame de Pandas
        df = pd.DataFrame(data, index=[0])  # Datos de entrada deben ser un diccionario

        df_procesado = procesar_entrada(df)

        # Normalizar los datos con el mismo escalador usado en el entrenamiento
        df_scaled = scaler_entrada.fit_transform(df_procesado)
        if not df_scaled.shape[1] == 18:
            incor_col = {"461": f"Incorrect number of columns. No of columns sent: {df_scaled.shape[1]}"}
            return jsonify(incor_col), 461

        prediction_scaled = model.predict(df_scaled)

        # Desescalar la predicción (volver a la escala original)
        prediction_real = scaler.inverse_transform(prediction_scaled)

        # Enviar la respuesta en JSON
        response = {"predicted_price": float(prediction_real[0][0])}
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)})

# Ejecutar la API en modo debug
if __name__ == "__main__":
    app.run(debug=True)
