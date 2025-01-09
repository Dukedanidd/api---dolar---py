from flask import Flask, jsonify
import joblib
from scraper.scraper import scrap_values  # Importamos el scrapper desde la carpeta scrapper
import os
import numpy as np
import yfinance as yf

app = Flask(__name__)

# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
model_path = os.path.join(parent_dir, 'modelo', 'modelo.pkl')
config_path = os.path.join(parent_dir, 'modelo', 'config.pkl')

# Cargar el modelo y la configuración
model = joblib.load(model_path)
config = joblib.load(config_path)
window_size = config['window_size']

# Endpoint para hacer predicción
@app.route('/predict', methods=['GET'])
def predict():
    # Scrapeamos los valores actuales
    compra, venta = scrap_values()
    print(f"Valores originales - Compra: '{compra}', Venta: '{venta}'")
    
    if compra is None or venta is None:
        return jsonify({'error': 'No se pudieron obtener los valores de compra y venta'}), 400

    try:
        # Limpiamos los valores
        compra = float(compra.replace('$', '').replace(',', '').replace(' ', ''))
        venta = float(venta.replace('$', '').replace(',', '').replace(' ', ''))

        # Obtener datos históricos
        symbol = "USDMXN=X"
        data = yf.download(symbol, start="2020-01-01", end="2025-01-01")
        data_close = data['Close']

        # Preparar el input como se hizo en el entrenamiento
        latest_data = np.concatenate([
            data_close[-window_size:].values.reshape(-1),  # últimos 1000 valores
            [compra, venta]  # valores actuales
        ])

        # Obtener la predicción
        prediccion = model.predict([latest_data])

        return jsonify({
            'valores_actuales': {
                'compra': compra,
                'venta': venta
            },
            'prediccion': float(prediccion[0])
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': 'Error al procesar la predicción',
            'detalle': str(e)
        }), 400

# Ruta raíz
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'API is running',
        'endpoints': {
            '/predict': 'GET - Obtiene predicción del dólar'
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
