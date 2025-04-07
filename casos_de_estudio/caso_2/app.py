from tensorflow.keras.models import load_model
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Permitir CORS desde cualquier origen (para desarrollo local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia a ["http://localhost"] si solo quieres permitir el origen específico
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Cargar el modelo guardado
model = load_model("modelos/modelo_images.keras")

def preprocess_image(image: Image.Image):
    # Convertir a escala de grises, redimensionar a 28x28 y normalizar
    image = image.convert("L").resize((28, 28))
    image_array = np.array(image) / 255.0
    image_array = image_array.reshape(1, 28, 28, 1)
    return image_array

def predict_digit(image: Image.Image):
    preprocessed = preprocess_image(image)
    prediction = model.predict(preprocessed)
    predicted_class = np.argmax(prediction)
    return int(predicted_class)


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    predicted_digit = predict_digit(image)
    return {"predicted_digit": predicted_digit}

