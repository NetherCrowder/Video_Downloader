import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from backend.config import obtener_ruta_descarga, actualizar_ruta_descarga

import win32com.client  # Importamos pywin32

# Definimos colores similares a la ventana de inicio
COLOR_FONDO = get_color_from_hex("#2E3440")  # Gris oscuro
COLOR_TITULO = get_color_from_hex("#ECEFF4")  # Blanco azulado
COLOR_BOTONES = get_color_from_hex("#5E81AC")  # Azul claro
COLOR_BOTONES_SECUNDARIOS = get_color_from_hex("#4C566A")  # Gris azulado
COLOR_BOTONES_PELIGRO = get_color_from_hex("#BF616A")  # Rojo suave

# Cargar el diseño de la pantalla desde una cadena de texto
Builder.load_string('''
<SettingsScreen>:
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

        # Título de la pantalla
        Label:
            text: "Configuración"
            size_hint_y: None
            height: 60
            font_size: '32sp'
            bold: True
            color: root.titulo_color

        # Muestra la carpeta de descarga actual
        Label:
            id: current_folder_label
            text: "Carpeta actual: " + root.current_folder
            size_hint_y: None
            height: 40
            font_size: '16sp'
            color: root.titulo_color

        # Botón para cambiar la carpeta de descarga
        Button:
            text: "Cambiar carpeta de descarga"
            size_hint_y: None
            height: 50
            background_color: root.botones_color
            color: 1, 1, 1, 1
            font_size: '16sp'
            on_press: root.select_folder()

        # Botón para regresar a la pantalla principal
        Button:
            text: "Volver al inicio"
            size_hint_y: None
            height: 50
            background_color: root.botones_secundarios_color
            color: 1, 1, 1, 1
            font_size: '16sp'
            on_press: root.go_to_main()
''')

def select_folder_native():
    """
    Abre el diálogo nativo de Windows para seleccionar una carpeta utilizando pywin32.
    Retorna la ruta seleccionada o None si se cancela.
    """
    shell = win32com.client.Dispatch("Shell.Application")
    folder = shell.BrowseForFolder(0, "Selecciona la carpeta de descarga", 0, 0)
    if folder:
        # folder.Self.Path contiene la ruta seleccionada
        return folder.Self.Path
    return None

class SettingsScreen(Screen):
    # Definimos los colores como propiedades de la clase
    fondo_color = COLOR_FONDO
    titulo_color = COLOR_TITULO
    botones_color = COLOR_BOTONES
    botones_secundarios_color = COLOR_BOTONES_SECUNDARIOS
    botones_peligro_color = COLOR_BOTONES_PELIGRO

    # Se carga la carpeta actual desde la configuración
    current_folder = obtener_ruta_descarga()

    def select_folder(self):
        """
        Llama a la función que utiliza pywin32 para abrir el diálogo nativo de selección de carpetas.
        Si se selecciona una carpeta, actualiza la configuración.
        """
        nueva_ruta = select_folder_native()
        if nueva_ruta:
            actualizar_ruta_descarga(nueva_ruta)
            self.current_folder = nueva_ruta
            self.ids.current_folder_label.text = "Carpeta actual: " + self.current_folder

    def go_to_main(self):
        """
        Regresa a la pantalla principal.
        """
        self.manager.current = "main_screen"

# Configuración de la ventana (opcional)
Window.clearcolor = COLOR_FONDO
