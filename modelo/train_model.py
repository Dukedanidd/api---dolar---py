# model/train_model.py
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import matplotlib.pyplot as plt
from scraper.scraper import scrap_values

# Descargar los datos históricos de USD/MXN
symbol = "USDMXN=X"
data = yf.download(symbol, start="2020-01-01", end="2025-01-01")

# Preprocesar los datos
df = pd.DataFrame(data)
data_close = df['Close']

# Definir el tamaño de la ventana una sola vez al inicio
window_size = 1000

# Obtener los valores actuales del scraper
compra, venta = scrap_values()
print(f"Valores obtenidos del scraper - Compra: {compra}, Venta: {venta}")

# Verificar y convertir los valores del scraper
if compra is not None and venta is not None:
    compra_value = float(compra.replace('$', ''))
    venta_value = float(venta.replace('$', ''))
    print(f"Valores convertidos - Compra: {compra_value}, Venta: {venta_value}")
else:
    print("No se pudieron obtener valores del scraper")
    compra_value = venta_value = None

# Crear listas para almacenar características y etiquetas
X = []
y = []

# Creamos ventana deslizante
for i in range(window_size, len(data_close)):
    # Características: ventana de precios de cierre
    features = data_close[i-window_size:i].values.reshape(-1)
    
    if compra_value is not None and venta_value is not None:
        # Agregar valores de compra y venta del scraper
        features = np.concatenate([features, [compra_value, venta_value]])
    
    X.append(features)
    y.append(data_close.iloc[i])

print(f"Forma de X: {np.array(X).shape}")  # Para verificar la dimensión de los datos

# Convertir listas a arrays de numpy
X = np.array(X)
y = np.array(y)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Realizar predicciones
y_pred = model.predict(X_test)

# Mostrar el rendimiento del modelo
print(f"R^2 score: {model.score(X_test, y_test)}")

# Mostrar últimas predicciones y valores reales
print("\nÚltimas 10 predicciones vs valores reales:")
for i in range(-10, 0):
    print(f"Real: {y_test[i].item():.2f}, Predicción: {y_pred[i].item():.2f}, Diferencia: {abs(y_test[i].item() - y_pred[i].item()):.2f}")

# Hacer una predicción con los últimos datos disponibles
if compra_value is not None and venta_value is not None:
    latest_data = np.concatenate([
        data_close[-window_size:].values.reshape(-1),
        [compra_value, venta_value]
    ])
    next_day_pred = model.predict([latest_data])
    print("\nPredicción usando datos históricos y valores del scraper:")
    print(f"Predicción para el siguiente día: {float(next_day_pred[0]):.2f}")
    print(f"Valores actuales del scraper - Compra: {compra}, Venta: {venta}")
else:
    print("\nNo se pudo hacer la predicción con valores del scraper")

# Graficar los resultados
plt.figure(figsize=(15, 10))
plt.plot(y_test, color='blue', label='Real', linewidth=2)
plt.plot(y_pred, color='red', label='Predicción', linestyle='dashed', linewidth=2)
plt.title('Predicciones vs Valores Reales')
plt.xlabel('Días')
plt.ylabel('Precio del Dólar')
plt.legend()
plt.show()

# Guardar los datos de prueba y predicciones
df_test = pd.DataFrame({'Real': y_test, 'Predicción': y_pred})
df_test.to_csv('modelo/datos_prueba.csv', index=False)

# Guardar el modelo entrenado
joblib.dump(model, 'modelo/modelo.pkl')

