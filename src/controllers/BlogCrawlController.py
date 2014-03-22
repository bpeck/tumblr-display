class BlogCrawlController(object):
    
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