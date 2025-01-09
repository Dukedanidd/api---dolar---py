# model/train_model.py
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import matplotlib.pyplot as plt
from scraper.scraper import scrap_values

# Descargar los datos históricos de USD/MXN
symbol = "USDMXN=X"
data = yf.download(symbol, start="2020-01-01", end="2025-01-01")

# Preprocesar los datos (usamos solo el precio de cierre)
df = pd.DataFrame(data)
df = df[['Close']]  # Usamos solo la columna 'Close' para la predicción

# Obtener los valores actuales del scraper
compra, venta = scrap_values()

# Verificamos si obtuvimos los valores del scraper correctamente
if compra is not None and venta is not None:
    df['Compra'] = compra
    df['Venta'] = venta
else:
    print("Los valores del scraper no se obtuvieron correctamente. Usando datos históricos solamente.")

# Crear características y etiquetas
X = df[['Close', 'Compra', 'Venta']]  # Características
y = df['Close'].values  # Etiquetas (precio de cierre)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo
model = LinearRegression()

# Entrenar el modelo
model.fit(X_train, y_train)

# Guardar el modelo entrenado
joblib.dump(model, 'model/modelo.pkl')

# Realizar predicciones
y_pred = model.predict(X_test)

# Mostrar el rendimiento del modelo
print(f"R^2 score: {model.score(X_test, y_test)}")

# Graficar los resultados
plt.figure(figsize=(15, 10))
plt.plot(y_test, color='blue', label='Real', linewidth=2)
plt.plot(y_pred, color='red', label='Predicción', linestyle='dashed', linewidth=2)
plt.title('Predicciones vs Valores Reales')
plt.xlabel('Días')
plt.ylabel('Precio del Dólar')
plt.legend()
plt.show()

# Guardar el modelo entrenado en la carpeta 'modelo'
joblib.dump(model, 'modelo/modelo.pkl')
