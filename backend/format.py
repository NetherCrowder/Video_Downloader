from yt_dlp import YoutubeDL

def obtener_formatos_disponibles(url):
    """
    Obtiene los formatos disponibles para un video dado su URL.
    """
    ydl_opts = {
        'quiet': True,  # Evita que yt-dlp imprima en la consola
        'extract_flat': False,  # Permite obtener información detallada de los formatos
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formatos = info.get('formats', [])
            return formatos
        except Exception as e:
            print(f"Error al obtener los formatos: {e}")
            return []

def seleccionar_tipo_descarga():
    """
    Permite al usuario seleccionar el tipo de descarga: audio, video o video sin sonido.
    """
    print("\nSelecciona el tipo de descarga:")
    print("1. Video (con audio)")
    print("2. Audio (solo audio)")
    print("3. Video mudo (sin audio)")
    tipo = input("Introduce el número correspondiente: ").strip()

    if tipo == "1":
        return "video"
    elif tipo == "2":
        return "audio"
    elif tipo == "3":
        return "video_mudo"
    else:
        print("Opción inválida. Saliendo...")
        return None

def obtener_formato_descarga(url):
    """
    Obtiene el formato de descarga según el tipo seleccionado.
    """
    tipo = seleccionar_tipo_descarga()
    if not tipo:
        return None

    # Asignar el formato según el tipo seleccionado
    if tipo == "video":
        return "bestvideo+bestaudio/best"
    elif tipo == "audio":
        return "bestaudio"
    elif tipo == "video_mudo":
        return "bestvideo"

# Ejemplo de uso
if __name__ == "__main__":
    url = input("Introduce la URL del video: ")
    formato_seleccionado = obtener_formato_descarga(url)
    if formato_seleccionado:
        print(f"\nFormato seleccionado: {formato_seleccionado}")