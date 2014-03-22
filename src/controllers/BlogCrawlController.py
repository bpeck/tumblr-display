class BlogCrawlController(object):
    
    def __init__(self, view):
        self.view = view
        self.period = (view.SCROLL_SPEED * 1000) + (view.DISPLAY_SPEED * 1000)
        self.t = self.period

    def update(self, dT):
        if self.view.initialized:
            self.t -= dT
        if self.t <= 0:
            self.view.incPost()
            self.t = self.period