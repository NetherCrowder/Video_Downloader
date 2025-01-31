from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        layout.add_widget(Label(text="Gestión de Descargas"))

        self.btn_create = Button(text="Crear")
        self.btn_create.bind(on_press=self.go_to_create)
        self.btn_read = Button(text="Leer")
        self.btn_read.bind(on_press=self.go_to_read)

        layout.add_widget(self.btn_create)
        layout.add_widget(self.btn_read)

        self.add_widget(layout)

    def go_to_create(self, instance):
        self.manager.current = "download"

    def go_to_read(self, instance):
        self.manager.current = "view_media"