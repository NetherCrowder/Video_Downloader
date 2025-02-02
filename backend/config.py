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

def crear_carpeta_descargas(carpeta_base=None):
    """
    Crea una carpeta llamada 'DescargasVideos' en la carpeta base proporcionada.
    Si no se proporciona una carpeta base, usa la carpeta de Videos del sistema.
    """
    if carpeta_base is None:
        carpeta_base = obtener_carpeta_videos()
    
    carpeta_descargas = os.path.join(carpeta_base, "DescargasVideos")

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta_descargas):
        os.makedirs(carpeta_descargas)
        print(f"Carpeta creada: {carpeta_descargas}")

    # Crear subcarpetas para video, audio y video mudo dentro de 'DescargasVideos'
    subcarpetas = ["Videos", "Audios", "Videos mudos"]
    for subcarpeta in subcarpetas:
        ruta_subcarpeta = os.path.join(carpeta_descargas, subcarpeta)
        if not os.path.exists(ruta_subcarpeta):
            os.makedirs(ruta_subcarpeta)
            print(f"Subcarpeta creada: {ruta_subcarpeta}")

    return carpeta_descargas

def verificar_y_crear_subcarpetas(carpeta_base):
    """
    Verifica y crea las subcarpetas necesarias dentro de la carpeta base.
    """
    subcarpetas = ["Videos", "Audios", "Videos mudos"]
    for subcarpeta in subcarpetas:
        ruta_subcarpeta = os.path.join(carpeta_base, subcarpeta)
        if not os.path.exists(ruta_subcarpeta):
            os.makedirs(ruta_subcarpeta)
            print(f"Subcarpeta creada: {ruta_subcarpeta}")

def obtener_ruta_descarga():
    """
    Obtiene la ruta de descarga desde la configuración.
    Si no existe una configuración, usa la carpeta 'DescargasVideos'.
    """
    # Verificar si ya existe un archivo de configuración
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            ruta_descarga = config.get("ruta_descarga")
            print(f"Ruta de descarga cargada desde la configuración: {ruta_descarga}")
            verificar_y_crear_subcarpetas(ruta_descarga)
            return ruta_descarga

    # Si no existe, usar la carpeta 'DescargasVideos'
    ruta_descarga = crear_carpeta_descargas()

    # Guardar la ruta en el archivo de configuración
    config = {"ruta_descarga": ruta_descarga}
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

    print(f"Ruta de descarga guardada: {ruta_descarga}")
    verificar_y_crear_subcarpetas(ruta_descarga)
    return ruta_descarga

def actualizar_ruta_descarga(nueva_ruta):
    """
    Actualiza la ruta de descarga en el archivo de configuración.
    Si la nueva ruta es None, usa la carpeta 'DescargasVideos'.
    """
    if nueva_ruta is None:
        nueva_ruta = crear_carpeta_descargas()
    else:
        # Crear la carpeta 'DescargasVideos' en la nueva ruta
        nueva_ruta_descargas = os.path.join(nueva_ruta, "DescargasVideos")
        if not os.path.exists(nueva_ruta_descargas):
            os.makedirs(nueva_ruta_descargas)
            print(f"Carpeta creada: {nueva_ruta_descargas}")
        verificar_y_crear_subcarpetas(nueva_ruta_descargas)
        nueva_ruta = nueva_ruta_descargas

    config = {"ruta_descarga": nueva_ruta}
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)
    print(f"Ruta de descarga actualizada: {nueva_ruta}")

# Ejemplo de uso
#if __name__ == "__main__":
#    ruta = obtener_ruta_descarga()
#    print(f"La ruta de descarga configurada es: {ruta}")