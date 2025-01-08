# api---dolar---py
Este proyecto tiene como objetivo desarrollar un sistema para predecir el tipo de cambio del dólar en México, integrando datos obtenidos de web scraping y fuentes históricas con un modelo de Machine Learning, y exponiendo las predicciones a través de una API.

🛠️ Fase 1: Web Scraping
-------------------------------------------------------------------------------------------------------

Primero construiremos los scrapers de los bancos y del Diario Oficial de la Federación (DOF). Esto incluye:

🔍 Inspeccionar las páginas web de los bancos y del DOF para identificar cómo extraer los datos.

🧑‍💻 Crear scripts que recolecten los tipos de cambio.

📊 Almacenar los datos en un formato organizado (CSV o DataFrame) para su posterior uso en el modelo.


🤖 Fase 2: Machine Learning (en Google Colab)
-------------------------------------------------------------------------------------------------------

📂 Usaremos los datos obtenidos del web scraping y los combinaremos con datos históricos descargados de yfinance.

🧹 Limpiaremos, procesaremos y transformaremos los datos para el modelo.

🏋️ Entrenaremos un modelo de Machine Learning para predecir el tipo de cambio futuro.

💾 Guardaremos el modelo entrenado en un archivo (.pkl o .h5) para usarlo después en la API.


🌐 Fase 3: Creación de la API (en Flask)
-------------------------------------------------------------------------------------------------------

⚙️ Configuraremos la API en Flask para que reciba solicitudes y devuelva predicciones.

🤝 Integraremos el modelo de Machine Learning guardado para realizar las predicciones.

✅ Probaremos la API para asegurarnos de que responde correctamente.

Atte => Duke(Daniel Balderrama)
