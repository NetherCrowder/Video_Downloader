# Descargador de Videos

Este es un proyecto personal desarrollado como práctica para descargar archivos multimedia de plataformas en línea como YouTube, Facebook, Twitter (X) e Instagram. Actualmente, el proyecto soporta descargas desde YouTube, permitiendo descargar videos en formato de video, audio y video mudo.

## Características

- **Descarga de videos**: Soporta descargas de videos desde YouTube.
- **Formatos disponibles**:
  - Video (con audio).
  - Audio (solo audio).
  - Video mudo (sin audio).
- **Interfaz de línea de comandos (CLI)**: Fácil de usar desde la terminal.
- **Interfaz gráfica de usuario (GUI)**: Interfaz amigable desarrollada con Kivy.
- **Configuración personalizada**: Permite seleccionar la carpeta de descarga.
- **Visualización de descargas**: Permite navegar y reproducir los archivos descargados.

## Requisitos

- Python 3.8 o superior.
- Dependencias listadas en `requirements.txt`.

## Instalación

1. **Clona el repositorio**:
    ```sh
    git clone https://github.com/tu_usuario/descargador_de_videos.git
    cd descargador_de_videos
    ```

2. **Crea un entorno virtual**:
    ```sh
    python -m venv .venv
    ```

3. **Activa el entorno virtual**:
    - En Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - En macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```

4. **Instala las dependencias**:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

### Interfaz Gráfica (GUI)

1. **Ejecuta la aplicación**:
    ```sh
    python app.py
    ```

2. **Navega por las pantallas**:
    - **Pantalla Principal**: Desde aquí puedes acceder a las opciones de descarga, visualización y configuración.
    - **Pantalla de Descarga**: Introduce la URL del video y selecciona el formato de descarga.
    - **Pantalla de Visualización**: Navega y reproduce los archivos descargados.
    - **Pantalla de Configuración**: Selecciona la carpeta de descarga.

### Interfaz de Línea de Comandos (CLI)

1. **Ejecuta el script de descarga**:
    ```sh
    python backend/downloader.py
    ```

2. **Sigue las instrucciones en la terminal**:
    - Introduce la URL del video.
    - Selecciona el formato de descarga (video, audio, mudo).

## Estructura del Proyecto

- [app.py](http://_vscodecontentref_/2): Archivo principal para ejecutar la aplicación GUI.
- [backend](http://_vscodecontentref_/3): Contiene la lógica de descarga y configuración.
    - `config.py`: Maneja la configuración de la carpeta de descarga.
    - `downloader.py`: Contiene la lógica para descargar videos.
- [frontend](http://_vscodecontentref_/4): Contiene las vistas de la interfaz gráfica.
    - `views/`: Contiene las pantallas de la aplicación.
        - `main_screen.py`: Pantalla principal.
        - `download_screen.py`: Pantalla de descarga.
        - `view_media_screen.py`: Pantalla de visualización de descargas.
        - `settings_screen.py`: Pantalla de configuración.
- [requirements.txt](http://_vscodecontentref_/5): Lista de dependencias del proyecto.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue los siguientes pasos:

1. **Fork el repositorio**.
2. **Crea una nueva rama**:
    ```sh
    git checkout -b feature/nueva-funcionalidad
    ```
3. **Realiza tus cambios**.
4. **Haz commit de tus cambios**:
    ```sh
    git commit -m 'Agrega nueva funcionalidad'
    ```
5. **Sube tus cambios**:
    ```sh
    git push origin feature/nueva-funcionalidad
    ```
6. **Abre un Pull Request**.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Si tienes alguna pregunta o sugerencia, no dudes en contactarme:

Nombre: [NetherCrowder]

Email: [luisaaron1930@gmail.com]

GitHub: https://github.com/NetherCrowder