from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty

from backend.downloader import descargar_video, obtener_ruta_descarga_backend, obtener_formato_descarga

class DownloadScreen(Screen):
    estado = StringProperty("")  # Para mostrar mensajes de estado

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        layout.add_widget(Label(text="Introduce la URL del video:"))
        self.url_input = TextInput(hint_text="URL del video", multiline=False)
        layout.add_widget(self.url_input)

        layout.add_widget(Label(text="Selecciona el formato:"))
        self.format_spinner = Spinner(
            text='Seleccionar formato',
            values=('Video (con audio)', 'Audio (solo audio)', 'Video mudo (sin audio)')
        )
        layout.add_widget(self.format_spinner)

        self.estado_label = Label(text=self.estado)
        layout.add_widget(self.estado_label)

        self.download_button = Button(text="Descargar")
        self.download_button.bind(on_press=self.download)
        layout.add_widget(self.download_button)

        self.back_button = Button(text="Regresar")
        self.back_button.bind(on_press=self.go_back)
        layout.add_widget(self.back_button)

        self.add_widget(layout)

    def download(self, instance):
        url = self.url_input.text
        format_selected = self.format_spinner.text
        ruta_descarga = obtener_ruta_descarga_backend()
        self.estado = f"Descargando video desde URL: {url} con formato: {format_selected} en la ruta: {ruta_descarga}"
        self.estado_label.text = self.estado
        descargar_video(url, ruta_descarga, format_selected)
        self.estado = "¡Descarga completada!"
        self.estado_label.text = self.estado
        self.manager.get_screen('view_media').refresh_file_chooser()

    def go_back(self, instance):
        self.manager.current = "main"