from Screen import Screen
import pytumblr
from Settings import Settings
from views.MultiPhotoView import MultiPhotoView
from models.BlogModel import BlogModel
from controllers.BlogCrawlController import BlogCrawlController
from pygame import display
class MainScreen(Screen):
    def __init__(self):
        super(MainScreen, self).__init__()

        viewableArea = display.get_surface().get_size()

        self.sName = "TumblrFrame"

        client = pytumblr.TumblrRestClient(Settings.OAUTH_CONSUMER, Settings.SECRET)

        print "created tumblr client"

        self.rModel = BlogModel(client, 'dinakelberman')
        self.rView = MultiPhotoView(self.rModel, viewableArea)
        self.rController = BlogCrawlController(self.rView)

        self.insertDrawable(self.rView)
        self.tControllers.append(self.rController)