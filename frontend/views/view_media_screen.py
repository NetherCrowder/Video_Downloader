import os # Importa el módulo os para interactuar con el sistema operativo

from functools import partial # Importa la función partial para crear funciones parciales
from kivy.lang import Builder # Importa la clase Builder de Kivy
from kivy.uix.screenmanager import Screen # Importa la clase Screen de Kivy
from kivy.uix.boxlayout import BoxLayout # Importa la clase BoxLayout de Kivy
from kivy.uix.button import Button # Importa la clase Button de Kivy
from kivy.uix.label import Label # Importa la clase Label de Kivy
from kivy.uix.popup import Popup # Importa la clase Popup de Kivy
from kivy.uix.textinput import TextInput # Importa la clase TextInput de Kivy

from backend.config import obtener_ruta_descarga # Importa la función obtener_ruta_descarga de backend.config

# Carga el archivo de diseño de la pantalla ViewMediaScreen
Builder.load_string('''
<ViewMediaScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        # Botones de navegación
        BoxLayout:
            size_hint_y: None
            height: 40
            spacing: 10

            Button:
                text: "Principal"
                size_hint_x: None
                width: 150
                on_press: root.ir_a_principal()
            
            Button:
                text: "Descargar"
                size_hint_x: None
                width: 150
                on_press: root.ir_a_descargar()

            Button:
                id: retroceder_btn
                text: "Retroceder"
                size_hint_x: None
                width: 150
                disabled: True
                on_press: root.retroceder_carpeta()

        # Lista de archivos multimedia
        ScrollView:
            size_hint: (1, 1)
            GridLayout:
                id: grid_layout
                cols: 1
                spacing: 10
                size_hint_y: None
                height: self.minimum_height

        # Estado de la operación
        Label:
            id: estado_label
            text: ""
            size_hint_y: None
            height: 30
            font_size: 14
            color: 0, 0, 0, 1  # Color negro
''')

class ViewMediaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ruta_actual = obtener_ruta_descarga()  # Carpeta base "DescargasVideos"
        self.build_ui()

    def build_ui(self):
        """
        Construye la interfaz de usuario.
        """
        self.cargar_archivos()

    def cargar_archivos(self):
        """
        Carga todos los archivos y carpetas de la ruta actual.
        """
        grid_layout = self.ids.grid_layout
        grid_layout.clear_widgets()

        if os.path.exists(self.ruta_actual):
            for nombre in os.listdir(self.ruta_actual):
                ruta_completa = os.path.join(self.ruta_actual, nombre)
                archivo_layout = BoxLayout(size_hint_y=None, height=40)
                archivo_layout.add_widget(Label(text=nombre, size_hint_x=0.6))

                if os.path.isdir(ruta_completa):
                    # Botón para abrir carpetas
                    archivo_layout.add_widget(Button(
                        text="Abrir",
                        size_hint_x=0.2,
                        on_press=partial(self.abrir_carpeta, nombre)
                    ))
                else:
                    # Botón de reproducción para archivos
                    archivo_layout.add_widget(Button(
                        text="Reproducir",
                        size_hint_x=0.2,
                        on_press=partial(self.reproducir_archivo, nombre)
                    ))

                    # Botón de editar para archivos
                    archivo_layout.add_widget(Button(
                        text="Editar",
                        size_hint_x=0.1,
                        on_press=partial(self.editar_archivo, nombre)
                    ))

                    # Botón de eliminar para archivos
                    archivo_layout.add_widget(Button(
                        text="Eliminar",
                        size_hint_x=0.1,
                        on_press=partial(self.confirmar_eliminacion, nombre)
                    ))

                grid_layout.add_widget(archivo_layout)

        # Habilitar o deshabilitar el botón "Retroceder"
        self.ids.retroceder_btn.disabled = (self.ruta_actual == obtener_ruta_descarga())

    def abrir_carpeta(self, nombre_carpeta, _):
        """
        Abre una carpeta y actualiza la ruta actual.
        """
        nueva_ruta = os.path.join(self.ruta_actual, nombre_carpeta)
        if os.path.isdir(nueva_ruta):
            self.ruta_actual = nueva_ruta
            self.cargar_archivos()

    def retroceder_carpeta(self):
        """
        Retrocede a la carpeta anterior.
        """
        if self.ruta_actual != obtener_ruta_descarga():
            self.ruta_actual = os.path.dirname(self.ruta_actual)
            self.cargar_archivos()

    def reproducir_archivo(self, archivo, _):
        """
        Reproduce el archivo multimedia con el reproductor predeterminado del sistema.
        """
        ruta_completa = os.path.join(self.ruta_actual, archivo)
        os.startfile(ruta_completa)

    def archivo_en_uso(self, ruta_archivo):
        """
        Verifica si el archivo está siendo utilizado por otro proceso.
        """
        try:
            with open(ruta_archivo, 'a'):
                pass
            return False  # El archivo no está en uso
        except IOError:
            return True  # El archivo está en uso

    def editar_archivo(self, archivo, _):
        """
        Muestra una ventana emergente para editar la información del archivo.
        """
        nombre, extension = os.path.splitext(archivo)  # Separar nombre y extensión
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=f"Editando: {archivo}"))

        # Campo de texto para editar el nombre
        nuevo_nombre = TextInput(text=nombre, multiline=False)  # Solo el nombre sin extensión
        popup_layout.add_widget(nuevo_nombre)

        # Botón para guardar cambios
        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        popup = Popup(title="Editar Archivo", content=popup_layout, size_hint=(0.8, 0.4))

        btn_layout.add_widget(Button(
            text="Guardar",
            on_press=lambda btn: self.guardar_cambios(archivo, nuevo_nombre.text + extension, popup)  # Restaurar la extensión
        ))
        btn_layout.add_widget(Button(
            text="Cancelar",
            on_press=popup.dismiss
        ))
        popup_layout.add_widget(btn_layout)

        popup.open()

    def guardar_cambios(self, archivo_viejo, nuevo_nombre, popup):
        """
        Renombra el archivo con el nuevo nombre, manteniendo la extensión.
        """
        # Extraer la extensión del archivo original
        nombre, extension = os.path.splitext(archivo_viejo)

        # Añadir la extensión al nuevo nombre si no la tiene
        if not nuevo_nombre.endswith(extension):
            nuevo_nombre += extension

        ruta_vieja = os.path.join(self.ruta_actual, archivo_viejo)
        ruta_nueva = os.path.join(self.ruta_actual, nuevo_nombre)

        # Verificar si el archivo está en uso
        if self.archivo_en_uso(ruta_vieja):
            self.mostrar_error("El archivo está siendo utilizado por otro proceso.")
            return

        try:
            os.rename(ruta_vieja, ruta_nueva)
            self.cargar_archivos()  # Recargar la lista de archivos
        except Exception as e:
            self.mostrar_error(f"Error al renombrar el archivo: {e}")
        finally:
            popup.dismiss()  # Cerrar el Popup después de guardar

    def confirmar_eliminacion(self, archivo, _):
        """
        Muestra una ventana emergente para confirmar la eliminación del archivo.
        """
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=f"¿Eliminar {archivo}?"))

        # Botones de confirmación
        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        popup = Popup(title="Confirmar Eliminación", content=popup_layout, size_hint=(0.6, 0.3))

        btn_layout.add_widget(Button(
            text="Sí",
            on_press=lambda btn: self.eliminar_archivo(archivo, popup)
        ))
        btn_layout.add_widget(Button(
            text="No",
            on_press=popup.dismiss
        ))
        popup_layout.add_widget(btn_layout)

        popup.open()

    def eliminar_archivo(self, archivo, popup):
        """
        Elimina el archivo seleccionado.
        """
        ruta_completa = os.path.join(self.ruta_actual, archivo)

        # Verificar si el archivo está en uso
        if self.archivo_en_uso(ruta_completa):
            self.mostrar_error("El archivo está siendo utilizado por otro proceso.")
            return

        try:
            os.remove(ruta_completa)
            self.cargar_archivos()  # Recargar la lista de archivos
        except Exception as e:
            self.mostrar_error(f"Error al eliminar el archivo: {e}")
        finally:
            popup.dismiss()  # Cerrar el Popup después de eliminar
    
    def refresh_file_chooser(self):
        """
        Recarga la lista de archivos multimedia.
        """
        self.cargar_archivos()

    def mostrar_error(self, mensaje):
        """
        Muestra un mensaje de error en un Popup.
        """
        popup = Popup(title="Error", content=Label(text=mensaje), size_hint=(0.6, 0.3))
        popup.open()

    def ir_a_principal(self):
        """
        Navega a la ventana principal.
        """
        self.manager.current = 'main_screen'

    def ir_a_descargar(self):
        """
        Navega a la ventana de descarga.
        """
        self.manager.current = 'download_screen'