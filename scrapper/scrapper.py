import requests
from bs4 import BeautifulSoup

# URL de la pagina web que queremos scrapear
url = 'https://www.bbva.mx/personas/informacion-financiera-al-dia.html'

# Realizamos la peticion HTTP a la URL que usamos
response = requests.get(url)

# Vamos a verificar si la peticion fue buena con un if
if response.status_code == 200:
    # Aqui voy a analizar el contenido de la respuesta
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraemos los valores de compra y venta
    compra = soup.find('span', class_='text-right precio-c').text.strip()
    venta = soup.find('span', class_='text-left precio-c').text.strip()
    
    # Imprimimos los valores
    print(f"Compra: {compra}")
    print(f"Venta: {venta}")
else:
    print('No se pudo obtener la informacion')


