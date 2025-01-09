from flask import Flask, jsonify
import joblib
from scraper.scraper import scrap_values  # Importamos el scrapper desde la carpeta scrapper
import os

app = Flask(__name__)

# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta al modelo
model_path = os.path.join(os.path.dirname(current_dir), 'modelo', 'modelo.pkl')
# Cargar el modelo
model = joblib.load(model_path)

# Endpoint para hacer predicción
@app.route('/predict', methods=['GET'])
def predict():
    # Scrapeamos los valores de compra y venta
    compra, venta = scrap_values()
    print(f"Valores originales - Compra: '{compra}', Venta: '{venta}'")  # Debug log
    
    if compra is None or venta is None:
        return jsonify({'error': 'No se pudieron obtener los valores de compra y venta'}), 400

    # Convertir los valores a formato numérico
    try:
        # Limpiamos los valores de cualquier carácter especial
        compra = compra.replace('$', '').replace(',', '').replace(' ', '')
        venta = venta.replace('$', '').replace(',', '').replace(' ', '')
        
        print(f"Valores limpiados - Compra: '{compra}', Venta: '{venta}'")  # Debug log
        
        compra = float(compra)
        venta = float(venta)
        
        print(f"Valores convertidos - Compra: {compra}, Venta: {venta}")  # Debug log
    except (ValueError, AttributeError) as e:
        print(f"Error en la conversión: {str(e)}")  # Debug log
        return jsonify({
            'error': 'Los valores de compra y venta no son válidos',
            'valores_recibidos': {
                'compra': compra,
                'venta': venta
            }
        }), 400

    # Hacer la predicción usando el modelo
    prediction = model.predict([[compra, venta]])
    print(f"Predicción: {prediction[0]}")  # Debug log

    return jsonify({
        'prediccion_siguiente': float(prediction[0]),
        'valores_actuales': {
            'compra': compra,
            'venta': venta
        }
    })

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
