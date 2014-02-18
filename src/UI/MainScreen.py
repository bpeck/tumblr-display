from Screen import Screen
import pytumblr
from Settings import Settings
from views.MultiPhotoView import MultiPhotoView
from models.BlogModel import BlogModel
from controllers.BlogCrawlController import BlogCrawlController
class MainScreen(Screen):
    def __init__(self):
        super(MainScreen, self).__init__()

        self.sName = "TumblrFrame"

        client = pytumblr.TumblrRestClient(Settings.OAUTH_CONSUMER, Settings.SECRET)

        print "created tumblr client"

        self.rModel = BlogModel(client, 'dinakelberman')
        self.rView = MultiPhotoView(self.rModel)
        self.rController = BlogCrawlController(self.rView)

        self.insertDrawable(self.rView)
        self.tControllers.append(self.rController)