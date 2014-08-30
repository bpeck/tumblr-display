from AbstractRootController import AbstractRootController
from controllers.RootModelCommands import NextCommand

class BlogCrawlController(AbstractRootController):
    
    def __init__(self, view):
        self.view = view
        self.period = (view.SCROLL_SPEED * 1000) + (view.DISPLAY_SPEED * 1000)
        self.t = self.period

    def update(self, dT):
        # the view is usually not ready while it is waiting for
        # images to finish loading in
        if self.view.isReady():    
            self.t -= dT

            if self.t <= 0:
                self.view.incPost()
                self.t = self.period

    """ Overrides AbstractRootController """
    def handleCommand(self, command):
        if isinstance(command, NextCommand):
            self.t = 0
    
    """ Overrides AbstractRootController """
    def getInfo(self):
        info = {}
        p = float(self.period) / 1000.0
        info['how'] = "Incrementing posts every %.1f sec." % p
        return info