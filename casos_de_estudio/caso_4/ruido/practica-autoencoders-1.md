### **Práctica: Autoencoder para Eliminar Ruido en Imágenes**  

**Objetivo**: Entrenar un autoencoder convolucional para eliminar ruido Gaussiano de imágenes del dataset CIFAR-10.  

---

### **1. Configuración Inicial**  
**Objetivo**: Preparar el entorno y entender el dataset.  
**Tareas**:  
1. Instalar bibliotecas necesarias (ej: TensorFlow/Keras, NumPy, Matplotlib).  
2. Cargar el dataset CIFAR-10 usando la API de Keras.  
3. Explorar las imágenes:  
   - Visualizar 10 ejemplos aleatorios.  
   - Verificar dimensiones de las imágenes (ej: 32x32 píxeles, 3 canales RGB).  

**Pista**:  
- Usar `keras.datasets.cifar10.load_data()` para cargar el dataset.  
- Las etiquetas no son necesarias (autoencoders son no supervisados).  

---

### **2. Preparación de Datos**  
**Objetivo**: Generar versiones ruidosas de las imágenes para entrenamiento.  
**Tareas**:  
1. Normalizar los valores de píxeles al rango [0, 1].  
2. Crear un dataset "ruidoso":  
   - Añadir ruido Gaussiano (media=0, desviación estándar=0.1) a las imágenes originales.  
   - Asegurar que los valores de píxeles estén en [0, 1] después de añadir ruido.   `np.clip(imagen_con_ruido, 0., 1.)`
3. Dividir los datos en entrenamiento (50,000 imágenes) y prueba (10,000 imágenes).  
Ya viene pre-dividido por defecto en keras.datasets.cifar10.load_data(). No hace falta hacer la separación manual a menos que quieras definir un validation split adicional. Podrías aclarar esto.
```
from keras.datasets import cifar10

(x_train, _), (x_test, _) = cifar10.load_data()
```

**Pista**:  
- Usar `np.random.normal` para generar ruido.  
- Las imágenes originales serán el *target* (salida deseada), y las ruidosas el *input* del autoencoder.  

---

### **3. Diseño de la Arquitectura**  
**Objetivo**: Construir un autoencoder convolucional simétrico.  
**Tareas**:  
1. **Encoder**:  
   - Capas convolucionales (`Conv2D`) con activación ReLU.  
   - Reducir progresivamente las dimensiones espaciales (ej: 32x32 → 16x16 → 8x8).  
   - Capa final: "cuello de botella" (espacio latente).  
2. **Decoder**:  
   - Capas transpuestas (`Conv2DTranspose`) para reconstruir la imagen.  
   - Usar activación **sigmoid** en la última capa (rango [0, 1]).  

**Pista**:  
- Ejemplo de estructura:  
  ```
  Input → Conv2D(32, kernel=3x3) → MaxPooling → Conv2D(64, kernel=3x3) → Latent → Conv2DTranspose(...) → Output
  ```  
- Evitar capas demasiado profundas para no saturar la memoria.  

---

### **4. Entrenamiento del Modelo**  
**Objetivo**: Ajustar los pesos del autoencoder para minimizar el error de reconstrucción.  
**Tareas**:  
1. Compilar el modelo:  
   - Función de pérdida: **MSE** (Error Cuadrático Medio).  
   - Optimizador: **Adam** con learning rate=0.001.  
2. Entrenar con datos ruidosos como entrada y datos originales como target.  
   - Batch size: 64-128.  
   - Épocas: 20-30 (monitorear la pérdida para evitar overfitting).  (puedes utilizar EarlyStopping con paciencia de 3-5 épocas, para evitar entrenar de más innecesariamente.)
3. Guardar el modelo entrenado para evaluación.  

**Pista**:  
- Usar `ModelCheckpoint` para guardar el mejor modelo durante el entrenamiento.  
- Si la pérdida no disminuye, reducir el learning rate o ajustar la arquitectura.  

---

### **5. Evaluación y Visualización**  
**Objetivo**: Analizar la calidad de las reconstrucciones.  
**Tareas**:  
1. **Cuantitativa**: Calcular el **PSNR** (Peak Signal-to-Noise Ratio) entre imágenes originales y reconstruidas.  
   - Valores altos de PSNR indican mejor calidad.  
2. **Cualitativa**: Visualizar ejemplos de:  
   - Imagen original.  
   - Imagen ruidosa (input).  
   - Imagen reconstruida (output).  

**Pista**:  
- PSNR se calcula como:  
  ```
  psnr = 10 * np.log10(1.0 / (mse + 1e-8))
  ```  
- Usar `matplotlib.pyplot` para mostrar imágenes en una cuadrícula.  

---

### **6. Análisis Crítico**  
**Objetivo**: Reflexionar sobre los resultados y posibles mejoras.  
**Preguntas guía**:  
1. ¿En qué tipos de imágenes (ej: animales, vehículos) funciona mejor el modelo?  
2. ¿Qué ocurre si aumentamos la intensidad del ruido (ej: desviación estándar=0.2)?  
3. ¿Cómo afectaría añadir más capas al encoder/decoder?  
4. Propón una modificación para mejorar el modelo (ej: regularización, dropout).  

---

### **7. Entrega Final**  
**Entregables**:  
- Reporte breve (1 página) con:  
  - Descripción de la arquitectura usada (diagrama opcional).  
  - Gráficos de pérdida durante entrenamiento.  
  - PSNR promedio en el dataset de prueba.  
  - Visualización de 5 ejemplos de reconstrucción.  

---

### **Recursos Adicionales**  
- Documentación de Keras: [Guía de Autoencoders](https://keras.io/examples/generative/autoencoder/).  
- Tutorial de PSNR: [Cálculo e Interpretación](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio).  

