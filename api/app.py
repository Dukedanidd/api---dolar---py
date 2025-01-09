from flask import Flask, jsonify
import joblib
from scraper.scraper import get_scraper_data  # Importamos el scrapper desde la carpeta scrapper

app = Flask(__name__)

# Cargar el modelo entrenado desde la carpeta 'modelo'
model = joblib.load('../modelo/modelo.pkl')

# Endpoint para hacer predicción
@app.route('/predict', methods=['GET'])
def predict():
    # Scrapeamos los valores de compra y venta usando el scrapper
    compra, venta = get_scraper_data()
    
    if compra is None or venta is None:
        return jsonify({'error': 'No se pudieron obtener los valores de compra y venta'}), 400

    # Convertir los valores a formato numérico
    compra = float(compra.replace(',', ''))
    venta = float(venta.replace(',', ''))

    # Hacer la predicción usando el modelo
    prediction = model.predict([[compra, venta]])

    # Retornar la predicción como JSON
    return jsonify({'prediccion': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
