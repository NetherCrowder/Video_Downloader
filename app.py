from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from frontend.views.main_window import MainScreen
from frontend.views.download_screen import DownloadScreen
from frontend.views.view_media_screen import ViewMediaScreen

class VideoDownloaderApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(DownloadScreen(name="download"))
        sm.add_widget(ViewMediaScreen(name="view_media"))
        return sm

if __name__ == "__main__":
    VideoDownloaderApp().run()
