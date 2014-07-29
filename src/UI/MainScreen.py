from Screen import Screen
import pytumblr
from Settings import Settings
from views.BlogView import BlogView
from models.BlogModel import BlogModel
from controllers.BlogCrawlController import BlogCrawlController
from pygame import display

class MainScreen(Screen):
    def __init__(self, blog_name="rekall"):
        super(MainScreen, self).__init__()

        viewable_area = display.get_surface().get_size()

        self.name = "TumblrFrame"

        client = pytumblr.TumblrRestClient(Settings.OAUTH_CONSUMER, Settings.SECRET)

        self.model = BlogModel(client, blog_name)
        self.view = BlogView(self.model, viewable_area)
        self.controller = BlogCrawlController(self.view)

        self.insertDrawable(self.view)
        self.controllers.append(self.controller)