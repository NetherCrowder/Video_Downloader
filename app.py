from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from frontend.views.main_window import MainScreen
from frontend.views.download_screen import DownloadScreen
from frontend.views.view_media_screen import ViewMediaScreen
from frontend.views.test_interface import NewDownloadScreen

class VideoDownloaderApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(DownloadScreen(name="download"))
        sm.add_widget(ViewMediaScreen(name="view_media"))
        sm.add_widget(NewDownloadScreen(name="new_download"))
        return sm

if __name__ == "__main__":
    VideoDownloaderApp().run()
