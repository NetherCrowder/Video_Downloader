import os
from functools import partial
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from backend.config import obtener_ruta_descarga

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

<PopupEditar@Popup>:
    title: "Editar Archivo"
    size_hint: (0.8, 0.4)
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        Label:
            text: root.texto_archivo
            size_hint_y: None
            height: 30
            font_size: 14

        TextInput:
            id: nuevo_nombre
            text: root.nombre_actual
            multiline: False
            size_hint_y: None
            height: 40

        BoxLayout:
            size_hint_y: None
            height: 40
            spacing: 10

            Button:
                text: "Guardar"
                on_press: root.guardar_cambios(nuevo_nombre.text)

            Button:
                text: "Cancelar"
                on_press: root.dismiss()

<PopupEliminar@Popup>:
    title: "Confirmar Eliminación"
    size_hint: (0.6, 0.3)
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        Label:
            text: root.texto_confirmacion
            size_hint_y: None
            height: 30
            font_size: 14

        BoxLayout:
            size_hint_y: None
            height: 40
            spacing: 10

            Button:
                text: "Sí"
                on_press: root.confirmar_eliminacion()

            Button:
                text: "No"
                on_press: root.dismiss()
''')

class ViewMediaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ruta_descarga = obtener_ruta_descarga()
        self.build_ui()

    def build_ui(self):
        """
        Construye la interfaz de usuario.
        """
        self.cargar_archivos()

    def cargar_archivos(self):
        """
        Carga todos los archivos de la carpeta de descargas.
        """
        grid_layout = self.ids.grid_layout
        grid_layout.clear_widgets()
        if os.path.exists(self.ruta_descarga):
            for archivo in os.listdir(self.ruta_descarga):
                archivo_layout = BoxLayout(size_hint_y=None, height=40)
                archivo_layout.add_widget(Label(text=archivo, size_hint_x=0.6))

                # Botón de reproducción
                archivo_layout.add_widget(Button(
                    text="Reproducir",
                    size_hint_x=0.2,
                    on_press=partial(self.reproducir_archivo, archivo)
                ))

                # Botón de editar
                archivo_layout.add_widget(Button(
                    text="Editar",
                    size_hint_x=0.1,
                    on_press=partial(self.editar_archivo, archivo)
                ))

                # Botón de eliminar
                archivo_layout.add_widget(Button(
                    text="Eliminar",
                    size_hint_x=0.1,
                    on_press=partial(self.confirmar_eliminacion, archivo)
                ))

                grid_layout.add_widget(archivo_layout)

    def refresh_file_chooser(self):
        """
        Recarga la lista de archivos multimedia.
        """
        self.cargar_archivos()

    def reproducir_archivo(self, archivo, _):
        """
        Reproduce el archivo multimedia con el reproductor predeterminado del sistema.
        """
        ruta_completa = os.path.join(self.ruta_descarga, archivo)
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

        ruta_vieja = os.path.join(self.ruta_descarga, archivo_viejo)
        ruta_nueva = os.path.join(self.ruta_descarga, nuevo_nombre)

        # Verificar si el archivo está en uso
        if self.archivo_en_uso(ruta_vieja):
            self.mostrar_error("El archivo está siendo utilizado por otro proceso.")
            return

        try:
            os.rename(ruta_vieja, ruta_nueva)
            self.cargar_archivos()  # Recargar la lista de archivos
            self.manager.get_screen('view_media').refresh_file_chooser()
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
        ruta_completa = os.path.join(self.ruta_descarga, archivo)

        # Verificar si el archivo está en uso
        if self.archivo_en_uso(ruta_completa):
            self.mostrar_error("El archivo está siendo utilizado por otro proceso.")
            return

        try:
            os.remove(ruta_completa)
            self.cargar_archivos()  # Recargar la lista de archivos
            self.manager.get_screen('view_media').refresh_file_chooser()
        except Exception as e:
            self.mostrar_error(f"Error al eliminar el archivo: {e}")
        finally:
            popup.dismiss()  # Cerrar el Popup después de eliminar

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