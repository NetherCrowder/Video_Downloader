# Descargador de Videos

Este es un proyecto personal desarrollado como práctica para descargar archivos multimedia de plataformas en línea como YouTube, Facebook, Twitter (X) e Instagram. Actualmente, el proyecto soporta descargas desde YouTube, permitiendo descargar videos en formato de video, audio y video mudo.

## Características

- **Descarga de videos**: Soporta descargas de videos desde YouTube.
- **Formatos disponibles**:
  - Video (con audio).
  - Audio (solo audio).
  - Video mudo (sin audio).
- **Interfaz de línea de comandos (CLI)**: Fácil de usar desde la terminal.
- **Configuración personalizada**: Permite seleccionar la carpeta de descarga.

## Requisitos

- Python 3.8 o superior.
- Dependencias listadas en `requirements.txt`.

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/descargador_videos.git
   cd descargador_videos

2. **Crea un entorno virtual (opcional pero recomendado)**:
    python -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate

3. **Instala las dependencias**:
    pip install -r requirements.txt

## Uso:

1. **Ejecuta el programa**:
    python main.py

2. **Introduce la URL del video**:
    El programa te pedirá que introduzcas la URL del video que deseas descargar.

3. **Selecciona el tipo de descarga**:
    Elige entre video, audio o video mudo.

4. **Especifica la carpeta de descarga**:
    Introduce la ruta donde deseas guardar el archivo o deja el campo vacío para usar la carpeta actual.

## Dependencias

Las dependencias del proyecto están listadas en el archivo requirements.txt. Para instalarlas, ejecuta:

- pip install -r requirements.txt

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, sigue estos pasos:

Haz un fork del repositorio.

Crea una rama con tu nueva funcionalidad (git checkout -b nueva-funcionalidad).

Realiza tus cambios y haz commit (git commit -m 'Añade nueva funcionalidad').

Haz push a la rama (git push origin nueva-funcionalidad).

Abre un Pull Request.

## Contacto

Si tienes alguna pregunta o sugerencia, no dudes en contactarme:

Nombre: [Tu Nombre]

Email: [tu-email@example.com]

GitHub: https://github.com/tu-usuario