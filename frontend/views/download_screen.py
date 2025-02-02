import os # Para manejar archivos y carpetas
import tempfile # Para crear una carpeta temporal para la cache
import shutil  # Para eliminar la carpeta temporal de manera recursiva
import requests # Para descargar la miniatura del video
import threading  # Para manejar hilos

from kivy.uix.screenmanager import Screen # Para crear la pantalla de descarga
from kivy.lang import Builder # Para cargar el diseño de la pantalla
from kivy.properties import StringProperty, NumericProperty # Para actualizar la UI
from kivy.app import App  # Para manejar el cierre de la aplicación
from kivy.clock import Clock  # Para actualizar la UI desde el hilo principal

from yt_dlp import YoutubeDL  # Usar yt-dlp para obtener la URL de la miniatura

from backend.downloader import descargar_video, obtener_ruta_descarga_backend  # Importar la función de descarga

# Cargar el diseño de la pantalla desde una cadena de texto
Builder.load_string('''
<DownloadScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        # Barra de búsqueda y botón de buscar (arriba)
        BoxLayout:
            size_hint_y: None
            height: 40
            spacing: 10

            TextInput:
                id: url_input
                hint_text: "Introduce la URL del video"
                multiline: False

            Button:
                text: "Buscar"
                size_hint_x: None
                width: 100
                on_press: root.buscar_video(url_input.text)

        # Contenedor central (visualización y panel derecho)
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10

            # Cuadro de visualización (izquierda)
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.7  # Ocupa el 70% del ancho
                spacing: 10

                Image:
                    id: preview_image
                    source: ""
                    allow_stretch: True

            # Panel derecho (información del video y opciones de formato)
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.3  # Ocupa el 30% del ancho
                spacing: 10
                padding: 10

                # Información del video (arriba)
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 5

                    Label:
                        id: video_title
                        text: "Título: No disponible"
                        size_hint_y: None
                        height: 100
                        font_size: 14
                        bold: True

                    Label:
                        id: video_duration
                        text: "Duración: No disponible"
                        size_hint_y: None
                        height: 100
                        font_size: 14

                    Label:
                        id: video_author
                        text: "Autor: No disponible"
                        size_hint_y: None
                        height: 100
                        font_size: 14

                # Opciones de formato (abajo)
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 30

                    Label:
                        text: "Opciones de formato:"
                        size_hint_y: None
                        height: 30

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 40

                        CheckBox:
                            id: video_checkbox
                            group: "formato"
                            active: True

                        Label:
                            text: "Video"

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 40

                        CheckBox:
                            id: audio_checkbox
                            group: "formato"

                        Label:
                            text: "Audio"

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 40

                        CheckBox:
                            id: video_mudo_checkbox
                            group: "formato"

                        Label:
                            text: "Video mudo"

        # Barra de progreso y botón de descarga (abajo)
        BoxLayout:
            size_hint_y: None
            height: 40
            spacing: 10

            ProgressBar:
                id: progress_bar
                max: 100
                value: root.progreso

            Button:
                text: "Descargar"
                size_hint_x: None
                width: 150
                on_press: root.start_descargar(url_input.text)

        # Botones de navegación (abajo)
        BoxLayout:
            size_hint_y: None
            height: 40
            spacing: 10

            Button:
                text: "Regresar a Principal"
                size_hint_x: None
                width: 150
                on_press: root.regresar_a_principal()

            Button:
                text: "Ver Descargas"
                size_hint_x: None
                width: 150
                on_press: root.ir_a_visualizacion()
        
        # Estado de la descarga
        Label:
            id: estado_label
            text: ""
            size_hint_y: None
            height: 30
            font_size: 14
            color: 0, 0, 0, 1  # Color negro
''')

class DownloadScreen(Screen):
    progreso = NumericProperty(0)  # Progreso de la descarga (0-100)
    tiempo_restante_texto = StringProperty("00:00")  # Tiempo restante de la descarga
    miniatura_cache = None  # Ruta de la miniatura en cache
    cache_dir = None  # Carpeta temporal para la cache

    def buscar_video(self, url):
        """
        Busca el video, descarga la miniatura y muestra la información.
        """
        # Limpiar la miniatura y la carpeta temporal antes de buscar un nuevo video
        self.limpiar_cache()

        if not url:
            return

        try:
            # Crear una carpeta temporal para la cache
            self.cache_dir = tempfile.mkdtemp(prefix="video_downloader_")

            # Configuración de yt-dlp para extraer la información del video
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                miniatura_url = info.get('thumbnail')

                # Mostrar la información del video
                self.ids.video_title.text = f"Título: {info.get('title', 'No disponible')}"
                self.ids.video_duration.text = f"Duración: {info.get('duration', 'No disponible')} segundos"
                self.ids.video_author.text = f"Autor: {info.get('uploader', 'No disponible')}"

                if miniatura_url:
                    # Descargar la miniatura usando requests
                    miniatura_path = os.path.join(self.cache_dir, 'miniatura.jpg')
                    response = requests.get(miniatura_url)
                    if response.status_code == 200:
                        with open(miniatura_path, 'wb') as f:
                            f.write(response.content)

                        # Mostrar la miniatura en la interfaz
                        self.ids.preview_image.source = miniatura_path
                        self.miniatura_cache = miniatura_path
                    else:
                        print(f"Error al descargar la miniatura: {response.status_code}")
                        self.limpiar_cache()
                else:
                    print("Error: No se pudo obtener la URL de la miniatura.")
                    self.limpiar_cache()
        except Exception as e:
            print(f"Error al obtener la miniatura: {e}")
            self.limpiar_cache()

    def limpiar_cache(self):
        """
        Limpia la miniatura, la información del video y la carpeta temporal.
        """
        if self.miniatura_cache and os.path.exists(self.miniatura_cache):
            os.remove(self.miniatura_cache)  # Eliminar la miniatura de la cache
        self.ids.preview_image.source = ""  # Limpiar la imagen en la interfaz
        self.miniatura_cache = None

        # Limpiar la información del video
        self.ids.video_title.text = "Título: No disponible"
        self.ids.video_duration.text = "Duración: No disponible"
        self.ids.video_author.text = "Autor: No disponible"

        # Eliminar la carpeta temporal si existe
        if self.cache_dir and os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        self.cache_dir = None

    def start_descargar(self, url):
        """
        Descarga el video con la URL y el formato seleccionado en un hilo separado.
        """
        # Limpiar la cache antes de la descarga
        self.limpiar_cache()

        # Obtener el formato seleccionado
        formato = ""
        if self.ids.video_checkbox.active:
            formato = "video"  # Formato para video con audio
        elif self.ids.audio_checkbox.active:
            formato = "audio"  # Formato para solo audio
        elif self.ids.video_mudo_checkbox.active:
            formato = "mudo"  # Formato para video sin audio

        if not url or not formato:
            return

        # Obtener la ruta de descarga
        ruta_descarga = obtener_ruta_descarga_backend()

        # Actualizar el estado de la descarga
        if hasattr(self, 'ids') and 'estado_label' in self.ids:
            self.ids.estado_label.text = f"Descargando video desde URL: {url} con formato: {formato} en la ruta: {ruta_descarga}"

        # Iniciar la descarga en un hilo separado
        threading.Thread(
            target=self._descargar_en_hilo,  # Función que se ejecutará en el hilo
            args=(url, ruta_descarga, formato, self.actualizar_progreso),  # Argumentos para la función
            daemon=True  # El hilo se detendrá cuando la aplicación se cierre
        ).start()

    def _descargar_en_hilo(self, url, ruta_descarga, formato, callback_progreso):
        """
        Función que se ejecuta en un hilo separado para realizar la descarga.
        """
        try:
            # Iniciar la descarga
            self.progreso = 0
            self.tiempo_restante_texto = "Calculando..."

            # Llamar a la función de descarga con los 4 parámetros
            descargar_video(
                url,
                ruta_descarga,
                formato,
                callback_progreso=callback_progreso  # Pasar el callback de progreso
            )

            # Cuando la descarga termina, actualizar la UI
            Clock.schedule_once(lambda dt: self._finalizar_descarga(), 0)
        except Exception as e:
            # Manejar errores
            Clock.schedule_once(lambda dt: self._mostrar_error(e), 0)

    def actualizar_progreso(self, progreso, tiempo_restante):
        """
        Actualiza la barra de progreso y el tiempo restante.
        Este método es llamado desde el hilo de descarga.
        """
        # Usar Clock para actualizar la UI desde el hilo principal
        Clock.schedule_once(lambda dt: self._actualizar_ui_progreso(progreso, tiempo_restante), 0)

    def _actualizar_ui_progreso(self, progreso, tiempo_restante):
        """
        Actualiza la UI con el progreso y el tiempo restante.
        Este método se ejecuta en el hilo principal.
        """
        self.progreso = progreso
        self.tiempo_restante_texto = f"Tiempo restante: {tiempo_restante} segundos"

    def _finalizar_descarga(self):
        """
        Finaliza la descarga y actualiza la UI.
        Este método se ejecuta en el hilo principal.
        """
        self.progreso = 100
        self.tiempo_restante_texto = "00:00"
        if hasattr(self, 'ids') and 'estado_label' in self.ids:
            self.ids.estado_label.text = "¡Descarga completada!"

        # Redireccionar a la pantalla de visualización y refrescar el file chooser
        self.manager.current = 'view_media_screen'
        self.manager.get_screen('view_media_screen').refresh_file_chooser()

    def _mostrar_error(self, error):
        """
        Muestra un mensaje de error en la UI.
        Este método se ejecuta en el hilo principal.
        """
        print(f"Error durante la descarga: {error}")
        if hasattr(self, 'ids') and 'estado_label' in self.ids:
            self.ids.estado_label.text = f"Error durante la descarga: {error}"

    def regresar_a_principal(self):
        """
        Regresa a la pantalla principal.
        """
        self.limpiar_cache()  # Limpiar la cache antes de cambiar de pantalla
        self.manager.current = 'main_screen'

    def ir_a_visualizacion(self):
        """
        Navega a la pantalla de visualización de descargas.
        """
        self.limpiar_cache()  # Limpiar la cache antes de cambiar de pantalla
        self.manager.current = 'view_media'

    def on_leave(self, *args):
        """
        Método que se ejecuta cuando el usuario abandona la pantalla.
        """
        self.limpiar_cache()  # Limpiar la cache al salir de la pantalla

    def on_stop(self):
        """
        Método que se ejecuta cuando la aplicación se cierra.
        """
        self.limpiar_cache()  # Limpiar la cache al cerrar la aplicación