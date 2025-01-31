import os
import subprocess
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput

from backend.config import obtener_ruta_descarga

class CustomFileChooser(FileChooserListView):
    def is_hidden(self, fn):
        try:
            return super().is_hidden(fn)
        except OSError as e:
            if e.errno == 32:  # ERROR_SHARING_VIOLATION
                return True
            else:
                raise

class ViewMediaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        layout.add_widget(Label(text="Archivos Multimedia"))

        ruta_descarga = obtener_ruta_descarga()
        print(f"Inicializando FileChooser en la ruta: {ruta_descarga}")
        self.file_chooser = CustomFileChooser(path=ruta_descarga)
        layout.add_widget(self.file_chooser)

        self.play_button = Button(text="Reproducir")
        self.play_button.bind(on_press=self.play_media)
        layout.add_widget(self.play_button)

        self.update_button = Button(text="Actualizar")
        self.update_button.bind(on_press=self.show_update_options)
        layout.add_widget(self.update_button)

        self.delete_button = Button(text="Eliminar")
        self.delete_button.bind(on_press=self.delete_media)
        layout.add_widget(self.delete_button)

        self.back_button = Button(text="Regresar")
        self.back_button.bind(on_press=self.go_back)
        layout.add_widget(self.back_button)

        self.add_widget(layout)

    def play_media(self, instance):
        selected_file = self.file_chooser.selection
        if selected_file:
            file_path = selected_file[0]
            if os.path.exists(file_path):
                if os.name == 'nt':  # Windows
                    os.startfile(file_path)
                elif os.name == 'posix':  # macOS or Linux
                    subprocess.call(('xdg-open', file_path))
                else:
                    print(f"No se puede abrir el archivo: {file_path}")
            else:
                print(f"Error: El archivo {file_path} no existe.")

    def show_update_options(self, instance):
        selected_file = self.file_chooser.selection
        if selected_file:
            self.update_layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
            self.update_layout.add_widget(Label(text="Nuevo nombre del archivo:"))
            self.new_name_input = TextInput(hint_text="Nuevo nombre", multiline=False)
            self.update_layout.add_widget(self.new_name_input)

            self.confirm_update_button = Button(text="Confirmar actualización")
            self.confirm_update_button.bind(on_press=self.update_media)
            self.update_layout.add_widget(self.confirm_update_button)

            self.add_widget(self.update_layout)

    def update_media(self, instance):
        selected_file = self.file_chooser.selection
        if selected_file:
            file_path = selected_file[0]
            new_name = self.new_name_input.text.strip()
            if new_name:
                new_path = os.path.join(os.path.dirname(file_path), new_name + os.path.splitext(file_path)[1])
                os.rename(file_path, new_path)
                self.file_chooser._update_files()
                print(f"Archivo renombrado a: {new_path}")
                self.remove_widget(self.update_layout)

    def delete_media(self, instance):
        selected_file = self.file_chooser.selection
        if selected_file:
            os.remove(selected_file[0])
            self.file_chooser._update_files()
            print(f"Eliminando archivo: {selected_file[0]}")

    def go_back(self, instance):
        self.manager.current = "main"