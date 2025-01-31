import os
import json
from pathlib import Path

# Ruta del archivo de configuración
CONFIG_FILE = "config.json"

def obtener_carpeta_videos():
    """
    Obtiene la ruta de la carpeta de Videos del sistema.
    """
    # Usamos Path para obtener la carpeta de Videos del usuario
    return str(Path.home() / "Videos")

def crear_carpeta_descargas():
    """
    Crea una carpeta llamada 'DescargasVideos' en la carpeta de Videos del sistema.
    """
    carpeta_videos = obtener_carpeta_videos()
    carpeta_descargas = os.path.join(carpeta_videos, "DescargasVideos")

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta_descargas):
        os.makedirs(carpeta_descargas)
        print(f"Carpeta creada: {carpeta_descargas}")

    return carpeta_descargas

def obtener_ruta_descarga():
    """
    Pide al usuario la ruta de descarga y la guarda en un archivo de configuración.
    Si ya existe una configuración, la carga.
    Si el usuario no especifica una ruta, usa la carpeta 'DescargasVideos'.
    """
    # Verificar si ya existe un archivo de configuración
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            ruta_descarga = config.get("ruta_descarga")
            print(f"Ruta de descarga cargada desde la configuración: {ruta_descarga}")
            return ruta_descarga

    # Si no existe, pedir al usuario la ruta de descarga
    ruta_descarga = input("Introduce la ruta donde deseas guardar los videos (deja vacío para usar la carpeta 'DescargasVideos'): ").strip()

    # Si el usuario no introduce una ruta, usar la carpeta 'DescargasVideos'
    if not ruta_descarga:
        ruta_descarga = crear_carpeta_descargas()

    # Guardar la ruta en el archivo de configuración
    config = {"ruta_descarga": ruta_descarga}
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

    print(f"Ruta de descarga guardada: {ruta_descarga}")
    return ruta_descarga

def cargar_configuracion():
    """
    Carga la configuración desde el archivo de configuración.
    Si no existe, devuelve un diccionario vacío.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}

def actualizar_ruta_descarga(nueva_ruta):
    """
    Actualiza la ruta de descarga en el archivo de configuración.
    """
    config = cargar_configuracion()
    config["ruta_descarga"] = nueva_ruta
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)
    print(f"Ruta de descarga actualizada: {nueva_ruta}")

# Ejemplo de uso
if __name__ == "__main__":
    ruta = obtener_ruta_descarga()
    print(f"La ruta de descarga configurada es: {ruta}")