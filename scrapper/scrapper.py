import requests
from bs4 import BeautifulSoup

# URL del iframe
iframe_url = 'https://bbv.infosel.com/bancomerindicators/indexV9.aspx'

# Función para leer los valores anteriores (si existen)
def read_last_values():
    try:
        with open('last_values.txt', 'r') as file:
            last_compra, last_venta = file.read().split('\n')
            return last_compra.strip(), last_venta.strip()
    except FileNotFoundError:
        return None, None  # Si el archivo no existe, no hay valores previos

# Función para guardar los valores actuales
def save_current_values(compra, venta):
    with open('last_values.txt', 'w') as file:
        file.write(f"{compra}\n{venta}")

# Realizamos la solicitud HTTP al iframe
response = requests.get(iframe_url)

if response.status_code == 200:
    # Analizamos el contenido del iframe
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Extraemos los valores de compra y venta
        compra = soup.select_one('body > section.indicadores.bg-divisas > div:nth-child(1) > div > div > div > div:nth-child(1) > div.d-flex > div.col.border-right > div:nth-child(2) > span').text.strip()
        venta = soup.select_one('body > section.indicadores.bg-divisas > div:nth-child(1) > div > div > div > div:nth-child(1) > div.d-flex > div:nth-child(2) > div:nth-child(2) > span').text.strip()

        # Leemos los valores anteriores
        last_compra, last_venta = read_last_values()

        # Verificamos si los valores han cambiado
        if compra != last_compra or venta != last_venta:
            print(f"¡Los valores han cambiado!\nCompra: {compra}\nVenta: {venta}")
            # Guardamos los nuevos valores
            save_current_values(compra, venta)
        else:
            print("Los valores no han cambiado.")

    except AttributeError:
        print("No se encontraron los valores dentro del iframe.")
else:
    print("No se pudo obtener la información del iframe.")
