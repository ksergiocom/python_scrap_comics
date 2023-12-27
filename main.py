import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def download_image(image_url, folder_path):
    print(f"Descargando {image_url}")
    """ Descarga una imagen y la guarda en la carpeta especificada. """
    try:
        response = requests.get(image_url, headers=HEADERS)
        response.raise_for_status()  # Asegura que la respuesta es exitosa

        # Crear el directorio si no existe
        os.makedirs(folder_path, exist_ok=True)

        # Guardar imagen
        image_path = os.path.join(folder_path, os.path.basename(urlparse(image_url).path))
        with open(image_path, 'wb') as file:
            file.write(response.content)

    except requests.RequestException:
        print(f"No se pudo descargar la imagen de {image_url}")

def clean_image_url(url):
    """ Limpia la URL de la imagen eliminando parámetros no deseados. """
    parsed_url = urlparse(url)
    clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    return clean_url

def download_images_from_page(url):
    print(f"Scrapeando pagina: {url}")
    """ Descarga todas las imágenes que coincidan con el patrón de una página web. """
    try:
        req = requests.get(url, headers=HEADERS)
        req.raise_for_status()  # Verificar que la respuesta sea exitosa

        soup = BeautifulSoup(req.text, "html.parser")
        images = soup.find_all('img')

        for img in images:
            src = img.get('src')
            if src and "arcaderage.co/wp-content/uploads/" in src:
                clean_src = clean_image_url(src)
                download_image(clean_src, download_folder)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return False  # Devuelve False si la página no existe
        else:
            raise
    return True  # Devuelve True si la página existe y se procesó correctamente

URL = "https://arcaderage.co"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
download_folder = "downloads"
page_count = 1

while True:
    page_url = URL if page_count == 1 else f"{URL}/page/{page_count}/"
    if not download_images_from_page(page_url):
        break  # Salir del bucle si la página no existe
    page_count += 1
