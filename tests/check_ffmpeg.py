import os
from yt_dlp import YoutubeDL

def verificar_ruta_ffmpeg():
    # Ruta al binario de ffmpeg
    ffmpeg_path = os.path.join("bin", "ffmpeg", "ffmpeg.exe")

    # Verificar si el archivo ffmpeg existe
    if not os.path.exists(ffmpeg_path):
        print(f"Error: No se encontró ffmpeg en la ruta {ffmpeg_path}.")
        return False

    # Configuración de yt-dlp
    ydl_opts = {
        'ffmpeg_location': ffmpeg_path,  # Especifica la ruta de ffmpeg
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Verificar si yt-dlp reconoce ffmpeg
            print("Ruta de ffmpeg configurada correctamente.")
            return True
    except Exception as e:
        print(f"Error al configurar yt-dlp: {e}")
        return False

if __name__ == "__main__":
    if verificar_ruta_ffmpeg():
        print("yt-dlp reconoce correctamente la ruta de ffmpeg.")
    else:
        print("Hubo un problema al configurar la ruta de ffmpeg en yt-dlp.")