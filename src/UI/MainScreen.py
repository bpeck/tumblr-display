from Screen import Screen
from Settings import Settings
from views.BlogView import BlogView
from models.BlogModel import BlogModel
from controllers.BlogCrawlController import BlogCrawlController
from pygame import display

class MainScreen(Screen):
    def __init__(self):
        super(MainScreen, self).__init__()

        self.name = "MainScreen"

        self._current_view = None

    @property
    def view(self):
        return self._current_view

    @view.setter
    def view(self, view):
        self._current_view = view

    def onDisplayChange(self, display_screen):
        if self._current_view:
            self._current_view.onResize(display_screen.get_rect())
