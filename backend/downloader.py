import os
from yt_dlp import YoutubeDL

from .config import obtener_ruta_descarga, verificar_y_crear_subcarpetas
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
    ruta_descarga = obtener_ruta_descarga()
    verificar_y_crear_subcarpetas(ruta_descarga)
    return ruta_descarga

def descargar_video(url, ruta_descarga, formato, callback_progreso=None):
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

    formato_id = obtener_formato_descarga(url, formato)
    if not formato_id:
        print("No se pudo seleccionar un formato.")
        return

    # Seleccionar la subcarpeta adecuada según el formato
    if formato == 'video':
        subcarpeta = 'Videos'
    elif formato == 'audio':
        subcarpeta = 'Audios'
    elif formato == 'mudo':
        subcarpeta = 'Videos mudos'
    else:
        print("Formato no reconocido.")
        return

    ruta_descarga_final = os.path.join(ruta_descarga, subcarpeta)

    # Configuración de yt-dlp
    ydl_opts = {
        'ffmpeg_location': ffmpeg_path,  # Especifica la ruta de ffmpeg
        'format': formato_id,  # Usa el formato seleccionado
        'outtmpl': os.path.join(ruta_descarga_final, '%(title)s.%(ext)s'),  # Ruta de descarga
        'quiet': True,  # Silencia las advertencias
        'progress_hooks': [lambda d: _progreso_descarga(d, callback_progreso)] if callback_progreso else []
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            print(f"Configurando yt-dlp con ffmpeg en: {ffmpeg_path}")
            ydl.download([url])
        print("¡Descarga completada correctamente!")
    except Exception as e:
        print(f"Error durante la descarga: {e}")

def _progreso_descarga(d, callback_progreso):
    """
    Hook de progreso para yt-dlp.
    Llama a callback_progreso con el progreso actual.
    """
    if callback_progreso and 'downloaded_bytes' in d and 'total_bytes' in d:
        # Calcular el progreso en porcentaje
        progreso = (d['downloaded_bytes'] / d['total_bytes']) * 100
        tiempo_restante = d.get('eta', 0)  # Tiempo restante en segundos
        callback_progreso(progreso, tiempo_restante)

if __name__ == "__main__":
    # Obtener la URL del video
    url = obtener_url()
    
    # Obtener la ruta de descarga
    ruta_descarga = obtener_ruta_descarga_backend()
    print(f"Descargando video en: {ruta_descarga}")
    
    # Seleccionar el formato (video, audio, mudo)
    formato = input("Introduce el formato (video, audio, mudo): ").strip()
    
    # Llamar a la función para descargar el video
    descargar_video(url, ruta_descarga, formato)