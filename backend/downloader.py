import os

from yt_dlp import YoutubeDL

from .config import obtener_ruta_descarga
from .format import obtener_formato_descarga

def obtener_url():
    """
    Pide al usuario la URL del video.
    """
    url = input("Introduce la URL del video: ").strip()
    return url

def obtener_ruta_descarga_backend():
    """
    Obtiene la ruta de descarga desde la configuración.
    """
    return obtener_ruta_descarga()

def descargar_video(url, ruta_descarga, format_selected):
    # Obtener la ruta absoluta del directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta absoluta al binario de ffmpeg
    ffmpeg_path = os.path.join(script_dir, "..", "bin", "ffmpeg", "ffmpeg.exe")

    # Verificar si el archivo ffmpeg existe
    if not os.path.exists(ffmpeg_path):
        print(f"Advertencia: No se encontró ffmpeg en la ruta {ffmpeg_path}.")
        return
    else:
        print(f"Advertencia: La ruta {ffmpeg_path} se reconoce correctamente.")

    formato_id = obtener_formato_descarga(url, format_selected)
    if not formato_id:
        print("No se pudo seleccionar un formato.")
        return

    # Configuración de yt-dlp
    ydl_opts = {
        'ffmpeg_location': ffmpeg_path,  # Especifica la ruta de ffmpeg
        'format': formato_id,  # Usa el formato seleccionado
        'outtmpl': os.path.join(ruta_descarga, '%(title)s.%(ext)s'),  # Ruta de descarga
        'quiet': True,  # Silencia las advertencias
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            print(f"Configurando yt-dlp con ffmpeg en: {ffmpeg_path}")
            ydl.download([url])
        print("¡Descarga completada correctamente!")
    except Exception as e:
        print(f"Error durante la descarga: {e}")

#if __name__ == "__main__":
    # Obtener la URL del video
#    url = obtener_url()
    
    # Obtener la ruta de descarga
#    ruta_descarga = obtener_ruta_descarga_backend()
#    print(f"Descargando video en: {ruta_descarga}")
    
    # Llamar a la función para descargar el video
#    descargar_video(url, ruta_descarga)