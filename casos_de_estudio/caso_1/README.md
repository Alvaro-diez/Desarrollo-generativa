# Funcionamiento de la API para predecir precios

En este directorio tendremos 2 archivos que tienen la información del modelo. 
- modelo_precio.h5
- modelo_precio.keras

Estos son nuestros modelos guardados del notebook `caso_estudio1.ipynb` que contiene todo el entrenamiento y visualización del modelo de predicción de precios que hemos creado.

Además tendremos un archivo llamado `scaler_price.pkl` que necesitamos para poder conseguir un resultado realista de los precios, ya que nuestro modelo para entrenarlo ha tenido que normalizarlo y necesitamos el mismo tipo de normalización para desnormalizarlo.

## Cómo ejecutar la API
Para ejecutar la API tenemos que abrir una terminal en el directorio donde se encuentra el archivo `app.py`. Para ejecutarlo hacemos:
```bash
python app.py
```
Con eso se habrá iniciado un servidor local Flask al que podremos hacer peticiones.

- Las peticiones se harán a nuestra propia ***IP (127.0.0.1)*** en el ***puerto 5000***.
- El endpoint del método POST para las predicciones es ***/predict***
- Le tendremos que pasar un total de **12 argumentos NO nulos** en formato *JSON*

Un ejemplo de llamada a la API sería este:
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"area": 8000, "bedrooms": 3, "bathrooms": 2, "stories": 2, "mainroad": 1, "guestroom": 0, "basement": 0, "hotwaterheating": 0, "airconditioning": 1, "parking": 2, "prefarea": 1, "furnishingstatus": 2}'
```
Es importante destacar que si estamos usando una terminal *cmd* de Windows probablemente nos salga un error. Esto se debe a las comillas dobles que no es capaz de hacer una buena separación. En caso de que el problema sea ese, ejecutar esto:
```cmd
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"area\": 8000, \"bedrooms\": 3, \"bathrooms\": 2, \"stories\": 2, \"mainroad\": 1, \"guestroom\": 0, \"basement\": 0, \"hotwaterheating\": 0, \"airconditioning\": 1, \"parking\": 2, \"prefarea\": 1, \"furnishingstatus\": 2}"

```
