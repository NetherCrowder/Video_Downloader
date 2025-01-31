import os
from yt_dlp import YoutubeDL

def verificar_ffmpeg():
    # Obtener la ruta absoluta del directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta absoluta al binario de ffmpeg
    ffmpeg_path = os.path.join(script_dir, "..", "bin", "ffmpeg", "ffmpeg.exe")

    # Verificar si el archivo ffmpeg existe
    if not os.path.exists(ffmpeg_path):
        print(f"Error: No se encontró ffmpeg en la ruta {ffmpeg_path}.")
        return False

    # Configuración de yt-dlp
    ydl_opts = {
        'ffmpeg_location': ffmpeg_path,  # Especifica la ruta de ffmpeg
        'quiet': True,  # Mostrar mensajes en la consola
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Verificar si yt-dlp reconoce ffmpeg
            print("Configurando yt-dlp con ffmpeg...")
            ydl.download(['https://www.youtube.com/watch?v=uV9CLLvX_5Q'])
        print("¡Descarga completada correctamente!")
        return True
    except Exception as e:
        print(f"Error durante la descarga: {e}")
        return False

if __name__ == "__main__":
    if verificar_ffmpeg():
        print("yt-dlp reconoce correctamente la ruta de ffmpeg.")
    else:
        print("Hubo un problema al configurar la ruta de ffmpeg en yt-dlp.")