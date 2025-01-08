import requests
from bs4 import BeautifulSoup

# URL del iframe
iframe_url = 'https://bbv.infosel.com/bancomerindicators/indexV9.aspx'

# Realizamos la solicitud HTTP al iframe
response = requests.get(iframe_url)

if response.status_code == 200:
    # Analizamos el contenido del iframe
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Usamos los selectores CSS para extraer los valores de compra y venta
    try:
        compra = soup.select_one('body > section.indicadores.bg-divisas > div:nth-child(1) > div > div > div > div:nth-child(1) > div.d-flex > div.col.border-right > div:nth-child(2) > span').text.strip()
        venta = soup.select_one('body > section.indicadores.bg-divisas > div:nth-child(1) > div > div > div > div:nth-child(1) > div.d-flex > div:nth-child(2) > div:nth-child(2) > span').text.strip()

        # Imprimimos los valores
        print(f"Compra: {compra}")
        print(f"Venta: {venta}")
    except AttributeError:
        print("No se encontraron los valores dentro del iframe.")
else:
    print("No se pudo obtener la información del iframe.")
