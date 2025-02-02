import os  # Módulo para trabajar con el sistema operativo
import json  # Módulo para trabajar con archivos JSON
import win32com.client  # pywin32 ya está instalado en tu proyecto

from kivy.app import App  # Importamos la clase App de Kivy
from kivy.uix.screenmanager import ScreenManager  # Importamos la clase ScreenManager de Kivy
from kivy.animation import Animation  # Importamos la clase Animation de Kivy

from backend.config import obtener_ruta_descarga, actualizar_ruta_descarga  # Funciones de configuración

CONFIG_FILE = "config.json"  # Nombre del archivo de configuración

def select_folder_native(title="Selecciona la carpeta de descarga"):
    """
    Abre el diálogo nativo de Windows para seleccionar una carpeta utilizando pywin32.
    Retorna la ruta seleccionada o None si se cancela.
    """
    try:
        shell = win32com.client.Dispatch("Shell.Application")  # Crea una instancia de la aplicación Shell
        folder = shell.BrowseForFolder(0, title, 0, 0)  # Abre el diálogo de selección de carpeta
        if folder:  # Si se selecciona una carpeta
            return folder.Self.Path  # Retorna la ruta seleccionada
    except Exception as e:  # Captura cualquier error que ocurra
        print(f"Error al abrir el diálogo de selección de carpeta: {e}")  # Imprime el error en consola
    return None  # Si se cancela la selección, retorna None

def ensure_config():
    """
    Verifica si existe el archivo de configuración (config.json). Si no existe, solicita al usuario
    la carpeta de descarga mediante el diálogo nativo y la guarda en el archivo de configuración.
    """
    try:
        if not os.path.exists(CONFIG_FILE):  # Si el archivo de configuración no existe
            nueva_ruta = select_folder_native("Selecciona la carpeta de descarga")  # Abre el diálogo de selección de carpeta
            if nueva_ruta:  # Si se selecciona una carpeta
                actualizar_ruta_descarga(nueva_ruta)  # Actualiza la ruta de descarga y crea las carpetas necesarias
            else:
                # Si no se selecciona ninguna carpeta, se usa la ruta por defecto
                ruta_descarga = obtener_ruta_descarga()  # Obtiene la ruta por defecto y crea las carpetas necesarias
                config = {"ruta_descarga": ruta_descarga}  # Crea un diccionario con la ruta por defecto
                with open(CONFIG_FILE, "w") as file:  # Abre el archivo en modo escritura
                    json.dump(config, file)  # Guarda la configuración en el archivo
                print(f"Ruta de descarga configurada: {config['ruta_descarga']}")  # Imprime la ruta en consola
    except Exception as e:  # Captura cualquier error que ocurra
        print(f"Error al crear o leer el archivo de configuración: {e}")  # Imprime el error en consola

class VideoDownloaderApp(App):
    title = "Coffee Media Studio"  # Título de la ventana de la aplicación
    icon = "frontend/assets/coffee_icon.ico"  # Icono de la ventana de la aplicación

    def build(self):
        """
        Construye la interfaz de usuario y configura el ScreenManager.
        """
        # Ruta de la imagen del logo
        logo_path = os.path.join(os.path.dirname(__file__), "frontend", "assets", "logo.png")
        logo_path = logo_path.replace('/', '\\')  # Reemplaza las barras inclinadas por barras invertidas
        self.logo_path = logo_path  # Guarda la ruta de la imagen del logo

        sm = ScreenManager()  # Crea una instancia del ScreenManager
        from frontend.views.main_screen import MainScreen  # Importamos la pantalla principal
        from frontend.views.download_screen import DownloadScreen  # Importamos la pantalla de descarga de medios
        from frontend.views.view_media_screen import ViewMediaScreen  # Importamos la pantalla de visualización de medios
        from frontend.views.settings_screen import SettingsScreen  # Importamos la pantalla de configuración

        # Agregamos las pantallas al ScreenManager
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(DownloadScreen(name="download_screen"))
        sm.add_widget(ViewMediaScreen(name="view_media_screen"))
        sm.add_widget(SettingsScreen(name="settings_screen"))

        return sm  # Retornamos el ScreenManager

    def on_start(self):
        """
        Método que se ejecuta al iniciar la aplicación.
        """
        # Animación de apertura: efecto fade in (transición de opacidad de 0 a 1 en 1.5 segundos)
        self.root.opacity = 0  # Opacidad inicial
        Animation(opacity=1, duration=1.5).start(self.root)  # Inicia la animación

if __name__ == "__main__":
    ensure_config()  # Verifica o crea el archivo de configuración antes de iniciar la app
    VideoDownloaderApp().run()  # Inicia la aplicación
