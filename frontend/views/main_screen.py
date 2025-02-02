import sys  # Para cerrar la aplicación

from kivy.uix.screenmanager import Screen  # Importamos la clase Screen de Kivy
from kivy.lang import Builder  # Importamos la clase Builder de Kivy
from kivy.core.window import Window  # Importamos la clase Window de Kivy
from kivy.utils import get_color_from_hex  # Importamos la función get_color_from_hex de Kivy

# Definimos colores en formato hexadecimal
COLOR_FONDO = get_color_from_hex("#2E3440")  # Gris oscuro
COLOR_TITULO = get_color_from_hex("#ECEFF4")  # Blanco azulado
COLOR_BOTONES = get_color_from_hex("#5E81AC")  # Azul claro
COLOR_BOTONES_SECUNDARIOS = get_color_from_hex("#4C566A")  # Gris azulado
COLOR_BOTONES_PELIGRO = get_color_from_hex("#BF616A")  # Rojo suave

# Cargar el diseño de la pantalla desde una cadena de texto
Builder.load_string('''
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        canvas.before:
            Color:
                rgba: root.fondo_color
            Rectangle:
                pos: self.pos
                size: self.size

        # Título de la aplicación (parte superior)
        Label:
            text: "COFFE MEDIA STUDIO"
            size_hint_y: None
            height: 60
            font_size: '32sp'
            bold: True
            color: root.titulo_color
            font_name: 'Roboto'  # Fuente moderna (asegúrate de tenerla instalada)

        # Contenedor principal (logo y botones)
        BoxLayout:
            orientation: 'horizontal'
            spacing: 20

            # Espacio para el logo (lado izquierdo)
            BoxLayout:
                orientation: 'horizontal'
                size_hint: 3, 1  # Logo más grande
                spacing: 10

                Image:
                    source: app.logo_path  # Ruta de la imagen del logo definida en app.py por el método build
                    size_hint: 1, 1
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            # Contenedor de botones (lado derecho)
            BoxLayout:
                orientation: 'vertical'
                spacing: 10
                size_hint: 1, 1
                pos_hint: {'top': 1}  # Centrar botones en la parte superior

                # Botones de acción
                Button:
                    text: "Descargar"
                    size_hint_y: None
                    height: 50
                    on_press: root.go_to_download()
                    background_color: root.botones_color
                    color: 1, 1, 1, 1  # Texto blanco
                    font_name: 'Roboto'
                    font_size: '16sp'

                Button:
                    text: "Visualización"
                    size_hint_y: None
                    height: 50
                    on_press: root.go_to_view()
                    background_color: root.botones_color
                    color: 1, 1, 1, 1  # Texto blanco
                    font_name: 'Roboto'
                    font_size: '16sp'

                Button:
                    text: "Configuración"
                    size_hint_y: None
                    height: 50
                    on_press: root.go_to_settings()
                    background_color: root.botones_secundarios_color
                    color: 1, 1, 1, 1  # Texto blanco
                    font_name: 'Roboto'
                    font_size: '16sp'

                Button:
                    text: "Cerrar"
                    size_hint_y: None
                    height: 50
                    on_press: root.close_app()
                    background_color: root.botones_peligro_color
                    color: 1, 1, 1, 1  # Texto blanco
                    font_name: 'Roboto'
                    font_size: '16sp'
''')

class MainScreen(Screen):
    # Definimos los colores como propiedades de la clase
    fondo_color = COLOR_FONDO
    titulo_color = COLOR_TITULO
    botones_color = COLOR_BOTONES
    botones_secundarios_color = COLOR_BOTONES_SECUNDARIOS
    botones_peligro_color = COLOR_BOTONES_PELIGRO

    def go_to_download(self):
        """
        Navega a la pantalla de descarga.
        """
        self.manager.current = "download_screen"

    def go_to_view(self):
        """
        Navega a la pantalla de visualización de descargas.
        """
        self.manager.current = "view_media_screen"

    def go_to_settings(self):
        """
        Navega a la pantalla de configuración.
        """
        self.manager.current = "settings_screen"

    def close_app(self):
        """
        Cierra la aplicación.
        """
        sys.exit()

# Configuración de la ventana
Window.clearcolor = COLOR_FONDO